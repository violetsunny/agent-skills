#!/usr/bin/env npx ts-node
/**
 * web-autopilot: Browser Recorder
 * Records all user interactions + network traffic through any web app.
 * Supports SSO login, multi-tab capture, REST/GraphQL/Form.
 * 
 * Copyright (c) 2026 徐柏雄 (xubx4)
 * 反馈/交流：xubx4@midea.com | 13824820932
 */

import { chromium, Browser, BrowserContext, Page, Request, Response } from 'playwright';
import * as fs from 'fs';
import * as path from 'path';
import * as readline from 'readline';
import { program } from 'commander';

// ─── Types ────────────────────────────────────────────────────────────────────

export interface CapturedRequest {
  id: string;
  seqNum: number;
  timestamp: number;
  relativeMs: number;
  method: string;
  url: string;
  headers: Record<string, string>;
  postData: string | null;
  postDataParsed?: any;
  resourceType: string;
}

export interface CapturedResponse {
  requestId: string;
  timestamp: number;
  status: number;
  statusText: string;
  headers: Record<string, string>;
  mimeType: string;
  body: string | null;
  bodyParsed?: any;
  truncated: boolean;
  isRedirect: boolean;
  // v6.5: 下载特征标注（自动检测，不影响现有逻辑）
  isFileResponse?: boolean;       // 是否是文件流响应（Content-Type 或 Content-Disposition 判断）
  containsTaskId?: boolean;       // 响应体是否包含 taskId/jobId/docId 等异步任务字段
  taskIdField?: string;           // taskId 字段路径（如 "data.docId"）
  // v6.6: body 精简相关
  bodySummary?: {                 // body 摘要（当不保存完整 body 时使用）
    topLevelKeys: string[];       // 顶层 key 列表
    keyFields: Record<string, any>; // 关键字段值（id/token/status/code 等）
  };
  bodySaved?: boolean;            // 是否保存了完整 body
  bodySaveReason?: string;        // 保存原因（whiteList/consumed/fileResponse/taskId）
  // v8.3.0: 大数组截断信息
  arrayTruncated?: Array<{
    path: string;                 // 被截断的数组路径（如 "data.list"）
    originalCount: number;        // 原始元素数量（AI 用于判断数据规模）
    keptCount: number;            // 保留的元素数量（头尾各N个）
  }>;
  // v8.3.0: JSON字符串摘要信息
  stringSummarized?: Array<{
    path: string;                 // 被摘要的字符串路径
    originalSize: number;         // 原始字符串长度（字节）
    keyCount: number;             // JSON 解析后的字段数量
  }>;
}

export interface UserAction {
  seqNum: number;
  timestamp: number;
  relativeMs: number;
  type: 'navigate' | 'click' | 'input' | 'select' | 'submit' | 'keydown' | 'drag' | 'upload' | 'marker'
      | 'scroll' | 'mouseenter' | 'dblclick' | 'wheel' | 'focus' | 'blur' | 'resize' | 'contextmenu';
  url: string;
  target?: string;
  targetText?: string;
  targetType?: string;
  value?: string;
  label?: string;
  // ── Selector validation fields (added by enhanced recorder) ──
  selectorStable?: string;          // Upgraded stable selector (if raw is C/D grade)
  stabilityGrade?: 'S' | 'A' | 'B' | 'C' | 'D';  // Selector stability grade
  uniquenessMatch?: number;         // querySelectorAll match count (1 = unique)
  selectorStrategy?: string;          // Strategy used to make selector unique
  relatedApi?: string;              // Associated API call (e.g. "POST /api/search")
  dependsOnAction?: number;         // seqNum of prerequisite action (conditional rendering)
  appearsAfterAction?: boolean;     // Whether this element appeared after a prior action
  sensitiveField?: boolean;         // Whether this is a sensitive input (auto-redacted)
  // ── Keyboard event fields ──
  key?: string;                     // Key value (e.g. "Enter", "Tab", "a", "Escape")
  keyModifiers?: string[];          // Modifier keys (e.g. ["Ctrl", "Shift"])
  // ── Drag event fields ──
  dragSource?: string;              // Drag source element selector
  dragSourceText?: string;          // Drag source text content
  // ── Upload event fields ──
  fileName?: string;                // Uploaded file name
  fileSize?: number;                // Uploaded file size in bytes
  // ── iframe fields ──
  inIframe?: boolean;               // Whether action occurred inside an iframe
  frameUrl?: string;                // URL of the iframe where action occurred
  // ── Scroll event fields ──
  scrollTarget?: string;            // Scroll target: 'window' or element className
  scrollTop?: number;               // Vertical scroll position
  scrollDirection?: 'up' | 'down'; // Scroll direction
  // ── Mouseenter/Hover event fields ──
  hoverTarget?: string;             // Element being hovered
  hoverDuration?: number;           // How long hover lasted before next action (ms)
  triggeredByHover?: boolean;       // Whether next click was on a hover-revealed element
  // ── Click-trigger context field ──
  triggeredByClick?: string;        // Stable ID of the click that triggered a dropdown/popover
  // ── Dblclick event fields ──
  // (reuses click fields: target, targetText, targetType)
  // ── Wheel event fields ──
  wheelDeltaX?: number;             // Horizontal wheel delta
  wheelDeltaY?: number;             // Vertical wheel delta
  // ── Focus/Blur event fields ──
  focusDirection?: 'in' | 'out';   // Focus direction (focus=in, blur=out)
  // ── Resize event fields ──
  viewportWidth?: number;           // New viewport width
  viewportHeight?: number;          // New viewport height
  // ── Contextmenu event fields ──
  contextMenuTarget?: string;       // Right-click target element
  // ── v8.1.0: 混合策略新增字段 ──
  candidates?: Array<{              // 候选选择器列表
    selector: string;
    grade: 'S' | 'A' | 'B' | 'C' | 'D';
    matchCount: number;
    strategy: string;
    confidence: number;
  }>;
  confidence?: number;              // 选择器置信度（0~1）
}

// ─── Auth Clues Types ─────────────────────────────────────────────────────────

export interface AuthClues {
  collectedAt: string;
  url: string;
  urlAuthParams: Array<{ name: string; value: string }>;
  globalTokens: Record<string, string>;
  storageTokens: {
    localStorage: Record<string, string>;
    sessionStorage: Record<string, string>;
  };
  cookies: string;
  authHeaders: Record<string, { count: number; sampleValue: string }>;
  authType: string;
}

// ─── Download Types (v6.5) ────────────────────────────────────────────────────

export interface DownloadEvent {
  timestamp: number;
  relativeMs: number;
  url: string;
  suggestedFilename: string;
  mimeType: string;
  triggerActionSeq?: number;  // 关联到触发下载的操作 seqNum
  // v7.5.0: 实时保存下载文件
  savedPath?: string;         // 文件保存到录制目录的完整路径
  fileSize?: number;          // 文件大小（字节）
  headers?: string[];         // 表头（xlsx/csv 第一行）
  relatedRequestIds?: string[]; // 关联的 API 请求 ID（触发下载的请求）
}

// v7.5.0: 下载文件汇总（用于 recording.json 输出）
export interface DownloadedFile {
  index: number;              // 第几个下载（从1开始）
  fileName: string;           // 原始文件名
  savedPath: string;          // 保存路径
  fileSize: number;           // 文件大小
  headers: string[] | null;   // 表头
  downloadUrl: string;        // 下载 URL
  triggerActionSeq?: number;  // 触发操作序号
  relatedRequestIds: string[];// 关联 API 请求
  timestamp: number;          // 下载时间戳
}

export interface DownloadAnalysis {
  detected: boolean;
  type: 'direct' | 'async-task' | 'blob-url' | 'new-window' | 'iframe' | 'frontend-generate' | 'unknown' | null;
  confidence: 'high' | 'medium' | 'low' | null;
  evidence: string[];
  relatedRequestIds: string[];
  outputFile?: {
    name: string;
    mimeType: string;
  };
}

// ── v7.2: Download chain & polling detection ──────────────────────────────

export interface DownloadChainBetweenReq {
  id: string;
  seqNum: number;
  method: string;
  url: string;
  responseStatus: number;
  responseContentType: string;
  responsePreview: string;    // 响应体前 200 字符
  bridgeFields?: Record<string, string>;  // v7.3: 桥接字段（downloadUrl/fileName/taskId 等）
}

export interface BridgeEvidence {
  found: boolean;
  matchUrl?: string;          // 匹配到的中间请求 URL
  matchField?: string;        // 匹配到的字段路径
  matchValue?: string;        // 匹配到的值
}

export interface DownloadChain {
  exportReqId: string;
  exportUrl: string;
  exportMethod: string;
  exportResponseStatus: number;
  exportResponsePreview: string;
  downloadReqId: string;
  downloadUrl: string;
  downloadResponseStatus: number;
  betweenRequests: DownloadChainBetweenReq[];
  gapMs: number;
  bridgeEvidence?: BridgeEvidence;  // v7.3: 桥接验证结果
}

export interface PollingPattern {
  urlPath: string;
  method: string;
  count: number;
  avgIntervalMs: number;
  requestIds: string[];
  sampleUrl: string;
}

export interface Recording {
  version: '1.0';
  taskName: string;
  startTime: number;
  endTime: number;
  durationMs: number;
  ssoUrl: string;
  finalUrl: string;
  requests: CapturedRequest[];
  responses: Record<string, CapturedResponse>;
  actions: UserAction[];
  finalCookies: any[];
  finalLocalStorage: Record<string, string>;
  finalSessionStorage: Record<string, string>;
  notes: string[];
  authClues?: AuthClues;
  downloadEvents: DownloadEvent[];      // v6.5: 下载事件列表
  downloadAnalysis?: DownloadAnalysis;  // v6.5: 录制结束时的自动分析结果
  downloadChains?: DownloadChain[];     // v7.2: export→download 请求链
  pollingPatterns?: PollingPattern[];   // v7.2: 轮询模式检测
  downloadedFileHeaders?: string[] | null;  // v7.4.3: 下载文件的表头（用于 API 模式校验）
  downloadedFileName?: string | null;       // v7.4.3: 下载文件名
  downloadedFiles?: DownloadedFile[];       // v7.5.0: 所有下载文件的完整信息
}

// ─── Config ───────────────────────────────────────────────────────────────────

const SKIP_RESOURCE_TYPES = new Set(['image', 'stylesheet', 'font', 'media', 'eventsource', 'ping', 'script', 'document']);
const SKIP_URL_PATTERNS: RegExp[] = [
  /google-analytics\.com/, /googletagmanager\.com/, /analytics\./,
  /hotjar\.com/, /fullstory\.com/, /mixpanel\.com/, /segment\.io/,
  /sentry\.io/, /bugsnag\.com/, /logrocket\.com/,
  /\.woff2?($|\?)/, /\.ttf($|\?)/, /\.eot($|\?)/,
  /\.png($|\?)/, /\.jpe?g($|\?)/, /\.gif($|\?)/, /\.svg($|\?)/,
  /\.ico($|\?)/, /\.webp($|\?)/, /^data:/,
];
const MAX_BODY_SIZE = 500_000;  // v7.3.3: 200KB → 500KB，避免大数据响应被截断

// ─── Helpers ──────────────────────────────────────────────────────────────────

function shouldCapture(request: Request): boolean {
  if (SKIP_RESOURCE_TYPES.has(request.resourceType())) return false;
  const url = request.url();
  if (SKIP_URL_PATTERNS.some(p => p.test(url))) return false;
  return true;
}

function tryParseJSON(str: string | null): any {
  if (!str) return undefined;
  try { return JSON.parse(str); } catch { return undefined; }
}

function tryParseFormData(str: string | null): any {
  if (!str) return undefined;
  try {
    const params = new URLSearchParams(str);
    const obj: Record<string, string> = {};
    params.forEach((v, k) => { obj[k] = v; });
    return Object.keys(obj).length > 0 ? obj : undefined;
  } catch { return undefined; }
}

function extractPostData(request: Request): { raw: string | null; parsed: any } {
  const raw = request.postData();
  if (!raw) return { raw: null, parsed: undefined };
  const contentType = request.headers()['content-type'] || '';
  let parsed: any;
  if (contentType.includes('application/json')) {
    parsed = tryParseJSON(raw);
  } else if (contentType.includes('application/x-www-form-urlencoded')) {
    parsed = tryParseFormData(raw);
  } else if (contentType.includes('multipart/form-data')) {
    parsed = { _note: 'multipart/form-data - see raw postData' };
  }
  // v7.1: 业务 API 不截断 postData（olap/query 等请求体可达 15KB+）
  // 非业务 API 保持 10KB 截断
  const isBusinessApi = /\/api\//.test(request.url());
  const maxPostSize = isBusinessApi ? 200_000 : 10_000;
  return { raw: raw.length > maxPostSize ? raw.substring(0, maxPostSize) + '...[truncated]' : raw, parsed };
}

// ─── Data Filtering Helpers (v6.6) ────────────────────────────────────────────

/**
 * 提取 response body 摘要（只保留关键信息，不保存完整数据）
 * 用于减少文件体积，同时保留对操作识别有用的信息
 */
function extractBodySummary(bodyParsed: any): { topLevelKeys: string[]; keyFields: Record<string, any> } {
  if (!bodyParsed || typeof bodyParsed !== 'object') {
    return { topLevelKeys: [], keyFields: {} };
  }
  
  const topLevelKeys = Object.keys(bodyParsed);
  const keyFields: Record<string, any> = {};
  
  // 需要提取的关键字段模式（id/token/status/code/message 等）
  const KEY_FIELD_PATTERNS = [
    'id', 'token', 'status', 'code', 'message', 'msg', 'error', 'success', 
    'docid', 'taskid', 'jobid', 'result', 'data',
    // v7.3: 桥接字段模式（用于 export→download 关联追溯）
    'download', 'filename', 'filecode', 'filepath', 'fileurl',
    'asyncid', 'url', 'link', 'href'
  ];
  
  function extractKeyFields(obj: any, path: string = '', depth: number = 0) {
    if (depth > 3 || !obj || typeof obj !== 'object') return;
    
    for (const [key, value] of Object.entries(obj)) {
      const lowerKey = key.toLowerCase();
      const currentPath = path ? `${path}.${key}` : key;
      
      // 检查是否匹配关键字段模式
      if (KEY_FIELD_PATTERNS.some(p => lowerKey.includes(p))) {
        // 只保存简单类型的值，不保存大对象
        if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean' || value === null) {
          keyFields[currentPath] = value;
        } else if (Array.isArray(value) && value.length <= 5) {
          // 小数组也保存（如选项列表）
          keyFields[currentPath] = value;
        }
      }
      
      // 递归搜索子对象
      if (typeof value === 'object' && value !== null) {
        extractKeyFields(value, currentPath, depth + 1);
      }
    }
  }
  
  extractKeyFields(bodyParsed);
  return { topLevelKeys, keyFields };
}

/**
 * v8.3.0: 截断大响应体中的大数组
 * 
 * 触发条件（同时满足）：
 * 1. 响应体 > 60KB（sizeThreshold）
 * 2. 数组元素 >= 12 个（arrayThreshold）
 * 
 * 截断规则：
 * - 保留头尾各 3 个元素（共 6 个）
 * - 每个元素内部结构完整保留（所有字段）
 * - 外层 JSON 结构完整保留（所有嵌套对象、非数组字段）
 * - 完整响应体仍保存在 recording-bodies.jsonl
 * 
 * 返回：
 * - truncated: 是否进行了截断
 * - body: 截断后的响应体（或原始响应体）
 * - truncatedArrays: 被截断的数组信息列表（路径、原始数量、保留数量）
 */
function truncateLargeArrays(
  body: string, 
  sizeThreshold: number = 60 * 1024,  // 60KB
  arrayThreshold: number = 12,         // 12个元素
  keepCount: number = 3                // 头尾各3个
): { 
  truncated: boolean; 
  body: string; 
  truncatedArrays: Array<{ path: string; originalCount: number; keptCount: number }>;
} {
  const emptyResult = { truncated: false, body, truncatedArrays: [] };
  
  // 小于阈值，不截断
  if (body.length <= sizeThreshold) {
    return emptyResult;
  }

  // 尝试解析JSON
  let parsed: any;
  try {
    parsed = JSON.parse(body);
  } catch {
    return emptyResult;
  }

  const truncatedArrays: Array<{ path: string; originalCount: number; keptCount: number }> = [];

  // 遍历对象，截断所有 >arrayThreshold 的数组
  function traverseAndTruncate(obj: any, path: string, depth: number) {
    if (depth > 10 || !obj || typeof obj !== 'object') return;

    for (const [key, value] of Object.entries(obj)) {
      const currentPath = path ? `${path}.${key}` : key;
      
      if (Array.isArray(value) && value.length >= arrayThreshold) {
        // 截断这个数组：保留头尾各 keepCount 个
        const head = value.slice(0, keepCount);
        const tail = value.slice(-keepCount);
        obj[key] = [...head, ...tail];
        truncatedArrays.push({
          path: currentPath,
          originalCount: value.length,
          keptCount: keepCount * 2
        });
      } else if (typeof value === 'object' && value !== null) {
        // 递归处理子对象
        traverseAndTruncate(value, currentPath, depth + 1);
      }
    }
  }

  traverseAndTruncate(parsed, '', 0);

  if (truncatedArrays.length === 0) {
    return emptyResult;
  }

  return {
    truncated: true,
    body: JSON.stringify(parsed),
    truncatedArrays
  };
}

/**
 * v8.3.0: JSON 字符串摘要
 * 
 * 触发条件（同时满足）：
 * 1. 响应体 > 60KB（sizeThreshold）
 * 2. 字符串长度 > 5KB（stringThreshold）
 * 
 * 规则：
 * - 尝试解析为 JSON
 * - 解析成功 → 转为摘要对象（_summary + _keys + _preview）
 * - 解析失败 → 保持原样（不截断）
 * 
 * 摘要对象格式：
 * {
 *   "_summary": "JSON字符串(70000字符)，解析后包含19个字段",
 *   "_keys": { "fieldName": "size, type", ... },
 *   "_preview": "前200字符..."
 * }
 */
function summarizeJsonStrings(
  body: string,
  sizeThreshold: number = 60 * 1024,  // 60KB
  stringThreshold: number = 5 * 1024  // 5KB
): {
  summarized: boolean;
  body: string;
  summarizedStrings: Array<{ path: string; originalSize: number; keyCount: number }>;
} {
  const emptyResult = { summarized: false, body, summarizedStrings: [] };
  
  if (body.length <= sizeThreshold) return emptyResult;

  let parsed: any;
  try { parsed = JSON.parse(body); } catch { return emptyResult; }

  const summarizedStrings: Array<{ path: string; originalSize: number; keyCount: number }> = [];

  function traverse(obj: any, pathStr: string, depth: number) {
    if (depth > 12 || !obj || typeof obj !== 'object') return;

    if (Array.isArray(obj)) {
      for (let i = 0; i < obj.length; i++) {
        if (typeof obj[i] === 'string' && obj[i].length > stringThreshold) {
          try {
            const innerParsed = JSON.parse(obj[i]);
            const keys: Record<string, string> = {};
            for (const [k, v] of Object.entries(innerParsed)) {
              const s = JSON.stringify(v as any).length;
              const t = v === null ? 'null' 
                        : Array.isArray(v) ? `arr[${(v as any[]).length}]` 
                        : typeof v === 'object' ? `obj{${Object.keys(v as object).length}}` 
                        : typeof v;
              keys[k] = `${s > 1024 ? (s / 1024).toFixed(1) + 'KB' : s + 'B'}, ${t}`;
            }
            const origLen = obj[i].length;
            obj[i] = {
              _summary: `JSON字符串(${origLen}字符)，解析后包含${Object.keys(innerParsed).length}个字段`,
              _keys: keys,
              _preview: obj[i].substring(0, 200)
            };
            summarizedStrings.push({ path: `${pathStr}[${i}]`, originalSize: origLen, keyCount: Object.keys(innerParsed).length });
          } catch {
            // 解析失败，保持原样
          }
        } else if (typeof obj[i] === 'object' && obj[i] !== null) {
          traverse(obj[i], `${pathStr}[${i}]`, depth + 1);
        }
      }
    } else {
      for (const [key, value] of Object.entries(obj)) {
        const curPath = pathStr ? `${pathStr}.${key}` : key;
        if (typeof value === 'string' && (value as string).length > stringThreshold) {
          try {
            const innerParsed = JSON.parse(value as string);
            const keys: Record<string, string> = {};
            for (const [k, v] of Object.entries(innerParsed)) {
              const s = JSON.stringify(v as any).length;
              const t = v === null ? 'null' 
                        : Array.isArray(v) ? `arr[${(v as any[]).length}]` 
                        : typeof v === 'object' ? `obj{${Object.keys(v as object).length}}` 
                        : typeof v;
              keys[k] = `${s > 1024 ? (s / 1024).toFixed(1) + 'KB' : s + 'B'}, ${t}`;
            }
            const origLen = (value as string).length;
            obj[key] = {
              _summary: `JSON字符串(${origLen}字符)，解析后包含${Object.keys(innerParsed).length}个字段`,
              _keys: keys,
              _preview: (value as string).substring(0, 200)
            };
            summarizedStrings.push({ path: curPath, originalSize: origLen, keyCount: Object.keys(innerParsed).length });
          } catch {
            // 解析失败，保持原样
          }
        } else if (typeof value === 'object' && value !== null) {
          traverse(value, curPath, depth + 1);
        }
      }
    }
  }

  traverse(parsed, '', 0);

  if (summarizedStrings.length === 0) return emptyResult;

  return {
    summarized: true,
    body: JSON.stringify(parsed),
    summarizedStrings
  };
}

/**
 * 判断 URL 是否匹配白名单（需要保存完整 body 的 API）
 * v7.3.3: 扩展白名单，覆盖更多系统的 API 命名规范
 */
function isWhitelistedUrl(url: string): boolean {
  const WHITELIST_PATTERNS = [
    // 导出/下载类
    /export/i, /download/i, /output/i, /extract/i,
    // 创建/提交类
    /create/i, /submit/i, /save/i, /confirm/i, /approve/i,
    // 生成类
    /generate/i, /build/i,
    // 字典/枚举类（用于参数编码匹配）
    /dictionary/i, /enum/i, /options/i, /lookup/i,
    /query\w*type/i, /category/i, /config/i,
  ];
  return WHITELIST_PATTERNS.some(p => p.test(url));
}

/**
 * 过滤无用的 actions
 * 在 Action-API correlation 之后调用（因为需要 relatedApi 字段）
 */
function filterActions(actions: UserAction[]): UserAction[] {
  const result: UserAction[] = [];
  const seenTargets = new Map<string, number>(); // target → index in result
  
  for (let i = 0; i < actions.length; i++) {
    const a = actions[i];
    
    // ── mouseenter 过滤 ──
    if (a.type === 'mouseenter') {
      // v7.3.3: 1000ms → 1500ms，避免误过滤需要长 hover 才触发的菜单
      if ((a.hoverDuration || 0) < 1500 && !a.relatedApi) continue;
      
      // 同一个 target 只保留第一次（或保留有 relatedApi 的那次）
      const existingIdx = seenTargets.get(a.target || '');
      if (existingIdx !== undefined) {
        const existing = result[existingIdx];
        // 如果新的有 relatedApi 而旧的没有，替换
        if (a.relatedApi && !existing.relatedApi) {
          result[existingIdx] = a;
        }
        // 否则跳过（保留第一次）
        continue;
      }
      seenTargets.set(a.target || '', result.length);
    }
    
    // ── blur 过滤 ──
    // 无 relatedApi 的 blur 百分百没用（只是"离开输入框"，不触发业务逻辑）
    if (a.type === 'blur' && !a.relatedApi) continue;
    
    // ── focus 过滤 ──
    if (a.type === 'focus') {
      const nextAction = actions[i + 1];
      // 后紧跟 input（同一个 target，时间差 <500ms）→ 被 input 吸收
      if (nextAction && nextAction.type === 'input' && 
          nextAction.target === a.target &&
          nextAction.timestamp - a.timestamp < 500) {
        continue;
      }
      // 后紧跟 blur 且无 input → 用户"经过"了这个字段
      if (nextAction && nextAction.type === 'blur' && 
          nextAction.target === a.target) {
        continue;
      }
    }
    
    // ── wheel 过滤 ──
    // 无 relatedApi 的 wheel 百分百没用（纯前端缩放，不影响数据）
    if (a.type === 'wheel' && !a.relatedApi) continue;
    
    // ── scroll 过滤 ──
    if (a.type === 'scroll') {
      // 连续 scroll（同一个 scrollTarget，时间差 <1000ms）→ 只保留最后一个
      const nextAction = actions[i + 1];
      if (nextAction && nextAction.type === 'scroll' && 
          nextAction.scrollTarget === a.scrollTarget &&
          nextAction.timestamp - a.timestamp < 1000) {
        continue;
      }
    }
    
    result.push(a);
  }
  
  return result;
}

/**
 * 精简 request headers
 * 策略：排除已知的浏览器标准 headers，保留所有非标准 headers（可能是认证/业务相关的）
 * 
 * v7.3.2 改进：
 * - 不再只保留 X- 开头的 headers（有些系统用 srm-tab-id、Midea-Auth 等非 X- 前缀）
 * - 改为排除标准 headers 白名单，保留所有非标准的
 * - 这样无论目标系统用什么命名规范，都不会漏掉
 */
function filterHeaders(headers: Record<string, string>, authHeaderNames: string[]): Record<string, string> {
  // 浏览器自动添加的标准 headers（不需要保留）
  const STANDARD_HEADERS = new Set([
    // HTTP/2 伪 headers
    ':method', ':path', ':scheme', ':authority',
    // 标准请求 headers
    'accept', 'accept-language', 'accept-encoding', 'accept-charset',
    'cache-control', 'connection', 'content-length',
    'host', 'pragma',
    'upgrade-insecure-requests', 'user-agent',
    // Sec- 开头的浏览器安全 headers
    // (用前缀匹配，不在 Set 里单独列)
    // Cookie 单独处理（太长，截断保留）
    // v7.4.1: origin 和 referer 保留（某些系统校验 CSRF）
  ]);
  
  const result: Record<string, string> = {};
  for (const [name, value] of Object.entries(headers)) {
    const lowerName = name.toLowerCase();
    
    // cookie 截断保留（可能包含有用的 session 信息）
    if (lowerName === 'cookie') {
      result[name] = value.length > 200 ? value.substring(0, 200) + '...[truncated]' : value;
      continue;
    }
    
    // content-type 保留（判断请求格式）
    if (lowerName === 'content-type') {
      result[name] = value;
      continue;
    }
    
    // 排除标准 headers
    if (STANDARD_HEADERS.has(lowerName)) continue;
    
    // 排除 Sec- 开头的浏览器安全 headers
    if (lowerName.startsWith('sec-')) continue;
    
    // 排除 DNT / Upgrade / TE 等不相关的
    if (['dnt', 'upgrade', 'te', 'trailer', 'via', 'warning'].includes(lowerName)) continue;
    
    // 保留所有其他 headers（包括认证、自定义、业务相关的）
    result[name] = value;
  }
  
  return result;
}

// ─── Download Detection Helpers (v6.5) ────────────────────────────────────────

/**
 * 递归搜索 JSON 对象中的 taskId 类字段
 * 返回找到的字段路径（如 "data.docId"），未找到返回 null
 */
function findTaskIdField(obj: any, path: string = ''): string | null {
  if (!obj || typeof obj !== 'object') return null;
  
  const TASK_ID_FIELDS = [
    'taskId', 'jobId', 'asyncId', 'exportId', 'docId', 'downloadId', 'fileId',
    // v7.3.3: 扩展字段列表，覆盖更多系统的命名规范
    'requestId', 'batchId', 'reportId', 'traceId', 'asyncTaskId',
    'taskNo', 'jobNo', 'batchNo', 'exportNo',
  ];
  
  if (Array.isArray(obj)) {
    for (let i = 0; i < Math.min(obj.length, 10); i++) {
      const result = findTaskIdField(obj[i], `${path}[${i}]`);
      if (result) return result;
    }
    return null;
  }
  
  for (const [key, value] of Object.entries(obj)) {
    const currentPath = path ? `${path}.${key}` : key;
    
    // 检查是否是目标字段
    if (TASK_ID_FIELDS.some(f => key.toLowerCase() === f.toLowerCase()) && value) {
      return currentPath;
    }
    
    // 递归搜索子对象（限制深度避免循环引用）
    if (value && typeof value === 'object' && path.split('.').length < 5) {
      const result = findTaskIdField(value, currentPath);
      if (result) return result;
    }
  }
  
  return null;
}

/**
 * 检测响应是否是文件下载
 */
function isFileDownloadResponse(headers: Record<string, string>, mimeType: string): boolean {
  // 检查 Content-Disposition
  const contentDisposition = headers['content-disposition'] || '';
  if (contentDisposition.toLowerCase().includes('attachment')) return true;
  
  // 检查 Content-Type（文件类型）
  const fileMimePatterns = [
    /application\/octet-stream/,
    /application\/vnd\./,           // Excel, Word 等 Office 格式
    /application\/pdf/,
    /text\/csv/,
    /application\/zip/,
    /application\/xlsx/,
    /application\/msword/,
  ];
  if (fileMimePatterns.some(p => p.test(mimeType))) return true;
  
  return false;
}

/**
 * 综合分析下载类型（v6.5）
 * 决策树：
 *   有 download 事件？
 *   ├── 是 → 有包含 taskId 的响应？
 *   │   ├── 是 → async-task（高置信度）
 *   │   └── 否 → 有文件流响应（Content-Disposition）？
 *   │       ├── 是 → direct（高置信度）
 *   │       └── 否 → 有 Blob URL DOM 变化？
 *   │           ├── 是 → blob-url（中置信度）
 *   │           └── 否 → direct（低置信度，仅有 download 事件）
 *   └── 否 → 有文件流响应但没触发 download？
 *       ├── 是 → direct（可能是 page.goto 触发的）
 *       └── 否 → 有 iframe 创建？
 *           ├── 是 → iframe（低置信度）
 *           └── 否 → 未检测到下载
 */
function analyzeDownloadType(
  downloadEvents: DownloadEvent[],
  responses: Record<string, CapturedResponse>,
  domChanges: { iframeCreated: boolean; iframeSrcs: string[]; blobUrlAnchors: boolean }
): DownloadAnalysis {
  const result: DownloadAnalysis = {
    detected: false,
    type: null,
    confidence: null,
    evidence: [],
    relatedRequestIds: [],
  };

  // 找出所有文件响应和任务响应
  const fileResponseIds: string[] = [];
  const taskResponseIds: string[] = [];
  let taskIdField: string | undefined;

  for (const [id, resp] of Object.entries(responses)) {
    if (resp.isFileResponse) {
      fileResponseIds.push(id);
    }
    if (resp.containsTaskId && resp.taskIdField) {
      taskResponseIds.push(id);
      taskIdField = resp.taskIdField;
    }
  }

  const hasDownloadEvent = downloadEvents.length > 0;
  const hasFileResponse = fileResponseIds.length > 0;
  const hasTaskResponse = taskResponseIds.length > 0;
  const hasBlobUrl = domChanges.blobUrlAnchors;
  const hasIframe = domChanges.iframeCreated;
  
  // v7.2: 直接检查 download URL 是否为 blob: 前缀（Web 标准，不依赖 MutationObserver）
  // MutationObserver 是异步微任务，前端生成文件太快时来不及捕获 DOM 变化
  // 直接检查 download URL 更可靠，且 blob: 是所有前端生成文件的通用机制
  const hasBlobDownloadUrl = downloadEvents.some(dl => dl.url.startsWith('blob:'));

  // 决策树
  if (hasDownloadEvent) {
    result.detected = true;
    
    if (hasTaskResponse) {
      // async-task: 有 download 事件 + 有 taskId 响应
      result.type = 'async-task';
      result.confidence = 'high';
      result.evidence.push(`检测到 ${downloadEvents.length} 个下载事件`);
      result.evidence.push(`发现 ${taskResponseIds.length} 个异步任务响应 (taskId 字段: ${taskIdField})`);
      result.relatedRequestIds = taskResponseIds;
    } else if (hasBlobDownloadUrl && !hasFileResponse) {
      // v7.2: download URL 是 blob: 且无文件流响应 → 前端生成文件
      // 比 MutationObserver 更可靠，blob: 是 Web 标准（所有浏览器通用）
      result.type = 'frontend-generate';
      result.confidence = 'high';
      result.evidence.push(`检测到 ${downloadEvents.length} 个下载事件`);
      result.evidence.push(`Download URL 为 blob: 前缀（前端生成文件）`);
      result.evidence.push('无文件流响应，确认是前端 JS 生成（如 JSZip/SheetJS）');
    } else if (hasBlobUrl && !hasFileResponse) {
      // frontend-generate: 有 Blob URL DOM 变化但没有文件流响应 → 前端生成文件
      // v6.9 新增：QBI 等系统用 JSZip/SheetJS 在前端生成 xlsx
      result.type = 'frontend-generate';
      result.confidence = 'medium';
      result.evidence.push(`检测到 ${downloadEvents.length} 个下载事件`);
      result.evidence.push('检测到 Blob URL 创建，但无文件流响应');
      result.evidence.push('可能是前端用 JSZip/SheetJS 生成文件（需进一步验证数据源 API）');
    } else if (hasFileResponse) {
      // direct: 有 download 事件 + 有文件流响应
      result.type = 'direct';
      result.confidence = 'high';
      result.evidence.push(`检测到 ${downloadEvents.length} 个下载事件`);
      result.evidence.push(`发现 ${fileResponseIds.length} 个文件流响应`);
      result.relatedRequestIds = fileResponseIds;
    } else if (hasBlobUrl) {
      // blob-url: 有 download 事件 + 有 Blob URL DOM 变化（有文件响应但也有 Blob）
      result.type = 'blob-url';
      result.confidence = 'medium';
      result.evidence.push(`检测到 ${downloadEvents.length} 个下载事件`);
      result.evidence.push('检测到 Blob URL 锚点创建');
    } else {
      // direct (low confidence): 仅有 download 事件
      result.type = 'direct';
      result.confidence = 'low';
      result.evidence.push(`检测到 ${downloadEvents.length} 个下载事件（无明确文件响应）`);
    }
    
    // 记录输出文件信息
    if (downloadEvents.length > 0) {
      const dl = downloadEvents[0];
      result.outputFile = {
        name: dl.suggestedFilename,
        mimeType: dl.mimeType,
      };
    }
  } else if (hasFileResponse) {
    // direct: 有文件响应但没触发 download（可能是 page.goto 触发的）
    result.detected = true;
    result.type = 'direct';
    result.confidence = 'low';
    result.evidence.push(`发现 ${fileResponseIds.length} 个文件流响应（无 download 事件）`);
    result.relatedRequestIds = fileResponseIds;
  } else if (hasIframe) {
    // iframe: 有 iframe 创建（低置信度，需要进一步验证）
    result.detected = true;
    result.type = 'iframe';
    result.confidence = 'low';
    result.evidence.push('检测到 iframe 创建（可能是隐藏 iframe 下载，也可能是其他功能）');
    if (domChanges.iframeSrcs.length > 0) {
      result.evidence.push(`iframe src: ${domChanges.iframeSrcs[0]}`);
      // 检查 iframe src 是否包含下载相关关键词
      const src = domChanges.iframeSrcs[0].toLowerCase();
      if (src.includes('download') || src.includes('export') || src.includes('file')) {
        result.evidence.push('iframe src 包含下载相关关键词');
        result.confidence = 'medium';
      }
    }
  }

  return result;
}

// ─── v7.2: Download Chain & Polling Detection ────────────────────────────────

/**
 * 桥接字段关键词：用于从中间响应中提取可能的桥接字段
 */
const BRIDGE_FIELD_PATTERNS = [
  /download/i, /filename/i, /filecode/i, /filepath/i, /fileurl/i,
  /taskid/i, /jobid/i, /docid/i, /asyncid/i,
  /url/i, /link/i, /href/i,
  /msgid/i, /messageid/i
];

/**
 * 从响应体中提取桥接字段（downloadUrl/fileName/taskId 等）
 */
function extractBridgeFields(body: any, path: string = '', depth: number = 0): Record<string, string> {
  const fields: Record<string, string> = {};
  if (!body || typeof body !== 'object' || depth > 5) return fields;
  
  for (const [key, value] of Object.entries(body)) {
    const currentPath = path ? `${path}.${key}` : key;
    const lowerKey = key.toLowerCase();
    
    // 检查是否是桥接字段
    if (BRIDGE_FIELD_PATTERNS.some(p => p.test(lowerKey))) {
      if (typeof value === 'string' && value.length > 0 && value.length < 500) {
        fields[currentPath] = value;
      }
    }
    
    // 递归搜索子对象（数组只取前3个元素）
    if (typeof value === 'object' && value !== null) {
      if (Array.isArray(value)) {
        for (let i = 0; i < Math.min(value.length, 3); i++) {
          Object.assign(fields, extractBridgeFields(value[i], `${currentPath}[${i}]`, depth + 1));
        }
      } else {
        Object.assign(fields, extractBridgeFields(value, currentPath, depth + 1));
      }
    }
  }
  
  return fields;
}

/**
 * 在中间响应中搜索 download 参数值，验证关联
 */
function findBridgeEvidence(
  downloadReq: CapturedRequest,
  betweenReqs: DownloadChainBetweenReq[],
  responses: Record<string, CapturedResponse>
): BridgeEvidence {
  // 提取 download 请求的参数值
  const downloadParamValues: string[] = [];
  if (downloadReq.postDataParsed) {
    for (const value of Object.values(downloadReq.postDataParsed)) {
      if (typeof value === 'string' && value.length > 5 && value.length < 200) {
        downloadParamValues.push(value);
      }
    }
  }
  
  if (downloadParamValues.length === 0) {
    return { found: false };
  }
  
  // 在中间响应中搜索（优先用完整 body，其次用 bodySummary）
  for (const betweenReq of betweenReqs) {
    const resp = responses[betweenReq.id];
    if (!resp) continue;
    
    // 搜索完整 body
    if (resp.body) {
      for (const paramValue of downloadParamValues) {
        if (resp.body.includes(paramValue)) {
          // 找到匹配，尝试定位字段路径
          let matchField = '';
          try {
            const bodyObj = JSON.parse(resp.body);
            const bridgeFields = extractBridgeFields(bodyObj);
            for (const [fieldPath, fieldValue] of Object.entries(bridgeFields)) {
              if (fieldValue === paramValue) {
                matchField = fieldPath;
                break;
              }
            }
          } catch {}
          
          return {
            found: true,
            matchUrl: betweenReq.url,
            matchField: matchField || '(in response body)',
            matchValue: paramValue
          };
        }
      }
    }
    
    // v7.3: body 被精简，从 bodySummary 中搜索
    if (resp.bodySummary?.keyFields) {
      for (const [fieldPath, fieldValue] of Object.entries(resp.bodySummary.keyFields)) {
        if (typeof fieldValue !== 'string') continue;
        // 过滤掉太短的值（如 "1"、"true"），避免误匹配
        if (fieldValue.length < 10) continue;
        for (const paramValue of downloadParamValues) {
          if (fieldValue === paramValue || fieldValue.includes(paramValue) || paramValue.includes(fieldValue)) {
            return {
              found: true,
              matchUrl: betweenReq.url,
              matchField: fieldPath,
              matchValue: fieldValue
            };
          }
        }
      }
    }
  }
  
  return { found: false };
}

/**
 * 检测 export → download 之间的请求链。
 * 
 * v7.3 改进：
 * 1. 增加行为特征识别（当 URL 匹配不到 export 时）
 * 2. 提取中间响应的桥接字段
 * 3. 自动验证桥接字段与 download 参数的匹配
 */
function detectDownloadChains(
  requests: CapturedRequest[],
  responses: Record<string, CapturedResponse>,
  downloadEvents: DownloadEvent[],
  actions: UserAction[]
): DownloadChain[] {
  // 1. 找"导出触发"请求
  const EXPORT_URL_PATTERNS = [/export/i, /\/generate\b/i];
  
  let exportReqs = requests.filter(r =>
    r.method === 'POST' && EXPORT_URL_PATTERNS.some(p => p.test(r.url))
  );
  
  // v7.3: 行为特征识别（当 URL 匹配不到时）
  if (exportReqs.length === 0 && downloadEvents.length > 0) {
    const firstDownload = downloadEvents[0];
    
    // 找 click 操作后 2 秒内的 POST 请求，且响应 result/data 为 null
    for (const action of actions) {
      if (action.type !== 'click') continue;
      
      const nearbyPosts = requests.filter(r =>
        r.method === 'POST' &&
        r.timestamp > action.timestamp &&
        r.timestamp < action.timestamp + 2000 &&
        r.timestamp < firstDownload.timestamp
      );
      
      for (const post of nearbyPosts) {
        const resp = responses[post.id];
        if (resp?.body) {
          try {
            const body = JSON.parse(resp.body);
            // result/data 为 null → 可能是异步导出触发
            if (body.result === null || body.data === null) {
              // v7.3.1: 增加验证——后续 60 秒内必须有文件流响应
              // 避免误识别普通操作（如保存、提交）为导出
              const hasSubsequentFileResponse = requests.some(r => {
                const rResp = responses[r.id];
                return r.timestamp > post.timestamp &&
                       r.timestamp < post.timestamp + 60000 &&
                       rResp && (rResp.isFileResponse || 
                                 /octet-stream|application\/vnd\.|application\/zip|application\/xlsx/i.test(rResp.mimeType));
              });
              if (hasSubsequentFileResponse) {
                exportReqs.push(post);
              }
            }
          } catch {}
        }
      }
    }
  }

  // 2. 找"文件下载"请求：response 是文件流
  const downloadReqs = requests.filter(r => {
    const resp = responses[r.id];
    return resp && (resp.isFileResponse || /octet-stream|application\/vnd\.|application\/zip|application\/xlsx/i.test(resp.mimeType));
  });

  const chains: DownloadChain[] = [];

  for (const exp of exportReqs) {
    // 找 export 之后的第一个文件下载请求
    const subsequentDownloads = downloadReqs.filter(d => d.seqNum > exp.seqNum);
    if (subsequentDownloads.length === 0) continue;

    const firstDownload = subsequentDownloads[0];
    const expResp = responses[exp.id];
    const dlResp = responses[firstDownload.id];

    // 提取中间请求 + 桥接字段
    const betweenReqs = requests
      .filter(r => r.seqNum > exp.seqNum && r.seqNum < firstDownload.seqNum)
      .map(r => {
        const resp = responses[r.id];
        let bridgeFields: Record<string, string> | undefined;
        
        // 提取桥接字段
        if (resp?.body) {
          // 有完整 body，直接提取
          try {
            const bodyObj = JSON.parse(resp.body);
            bridgeFields = extractBridgeFields(bodyObj);
            if (Object.keys(bridgeFields).length === 0) bridgeFields = undefined;
          } catch {}
        } else if (resp?.bodySummary?.keyFields) {
          // v7.3: body 被精简，从 bodySummary 中提取桥接字段
          bridgeFields = {};
          for (const [fieldPath, fieldValue] of Object.entries(resp.bodySummary.keyFields)) {
            const lowerPath = fieldPath.toLowerCase();
            if (BRIDGE_FIELD_PATTERNS.some(p => p.test(lowerPath))) {
              if (typeof fieldValue === 'string' && fieldValue.length > 0 && fieldValue.length < 500) {
                bridgeFields[fieldPath] = fieldValue;
              }
            }
          }
          if (Object.keys(bridgeFields).length === 0) bridgeFields = undefined;
        }
        
        return {
          id: r.id,
          seqNum: r.seqNum,
          method: r.method,
          url: r.url,
          responseStatus: resp?.status || 0,
          responseContentType: resp?.mimeType || '',
          responsePreview: (resp?.body || '').substring(0, 200),
          bridgeFields
        };
      });

    // 只记录有中间请求的 chain（direct 模式下中间没有请求，不需要 chain）
    if (betweenReqs.length > 0) {
      // v7.3: 验证桥接
      const bridgeEvidence = findBridgeEvidence(firstDownload, betweenReqs, responses);
      
      chains.push({
        exportReqId: exp.id,
        exportUrl: exp.url,
        exportMethod: exp.method,
        exportResponseStatus: expResp?.status || 0,
        exportResponsePreview: (expResp?.body || '').substring(0, 200),
        downloadReqId: firstDownload.id,
        downloadUrl: firstDownload.url,
        downloadResponseStatus: dlResp?.status || 0,
        betweenRequests: betweenReqs,
        gapMs: firstDownload.timestamp - exp.timestamp,
        bridgeEvidence
      });
    }
  }

  return chains;
}

/**
 * 检测轮询模式：短时间内对同一 URL path 的重复请求。
 * 
 * 轮询是异步下载的常见中间环节（轮询任务状态、轮询消息通知等）。
 * 本函数自动识别轮询模式，帮助分析阶段判断关联机制。
 */
function detectPollingPatterns(requests: CapturedRequest[]): PollingPattern[] {
  // 按 URL path（不含 query string）+ method 分组
  const groups = new Map<string, CapturedRequest[]>();

  for (const req of requests) {
    try {
      const urlObj = new URL(req.url);
      const key = `${req.method} ${urlObj.pathname}`;
      const group = groups.get(key) || [];
      group.push(req);
      groups.set(key, group);
    } catch {
      // URL 解析失败，跳过
    }
  }

  const patterns: PollingPattern[] = [];

  for (const [key, reqs] of groups) {
    if (reqs.length < 3) continue;  // 至少 3 次才算轮询

    // 按时间排序
    reqs.sort((a, b) => a.timestamp - b.timestamp);

    // 计算相邻请求的间隔
    const intervals: number[] = [];
    for (let i = 1; i < reqs.length; i++) {
      intervals.push(reqs[i].timestamp - reqs[i - 1].timestamp);
    }
    const avgInterval = intervals.reduce((a, b) => a + b, 0) / intervals.length;

    // 平均间隔 < 10 秒 → 判定为轮询
    if (avgInterval < 10000) {
      const [method, urlPath] = key.split(' ', 2);
      patterns.push({
        urlPath,
        method,
        count: reqs.length,
        avgIntervalMs: Math.round(avgInterval),
        requestIds: reqs.map(r => r.id),
        sampleUrl: reqs[0].url,
      });
    }
  }

  return patterns;
}

// ─── Auth Clues Collection ────────────────────────────────────────────────────

/**
 * 脱敏值：只显示前4位和后4位
 */
function maskValue(value: any): string {
  if (!value || typeof value !== 'string') return String(value);
  if (value.length <= 8) return '***';
  return value.substring(0, 4) + '***' + value.substring(value.length - 4);
}

/**
 * 从URL参数中提取认证相关参数
 * v7.3.3: 扩展认证参数名列表，覆盖更多系统的命名规范
 */
function extractUrlAuthParams(url: string): Array<{ name: string; value: string }> {
  const params: Array<{ name: string; value: string }> = [];
  try {
    const urlObj = new URL(url);
    const authParamNames = [
      'ticket', 'token', 'key', 'apikey', 'access_token', 
      'auth', 'session', 'sid', 'accessticket', 'accesstoken',
      // v7.3.3: 扩展列表
      'appid', 'sign', 'signature', 'credential',
      'jwt', 'bearer', 'oauth', 'nonce',
    ];
    
    for (const [name, value] of urlObj.searchParams.entries()) {
      const lowerName = name.toLowerCase();
      // 检查是否是已知的认证参数名
      if (authParamNames.some(n => lowerName.includes(n)) ||
          lowerName.includes('token') ||
          lowerName.includes('ticket') ||
          lowerName.includes('key') ||
          lowerName.includes('auth')) {
        params.push({ name, value: maskValue(value) });
      }
    }
  } catch {}
  return params;
}

/**
 * 从请求中提取认证header（找出所有业务请求共有的非标准header）
 * v7.3.3: 阈值从 80% 降低到 50%，并增加值一致性检查
 */
function extractAuthHeaders(requests: CapturedRequest[]): Record<string, { count: number; sampleValue: string }> {
  // 过滤出业务请求
  const businessRequests = requests.filter(r => 
    r.resourceType === 'xhr' || r.resourceType === 'fetch'
  );
  
  if (businessRequests.length === 0) return {};
  
  // 已知的非认证header（白名单）
  const nonAuthHeaders = new Set([
    'content-type', 'accept', 'accept-language', 'accept-encoding',
    'user-agent', 'sec-ch-ua', 'sec-ch-ua-mobile', 'sec-ch-ua-platform',
    'sec-fetch-dest', 'sec-fetch-mode', 'sec-fetch-site',
    'x-requested-with',  // Ajax标识，不是认证
    'referer', 'origin', 'content-length', 'connection',
    'cache-control', 'pragma', 'expires'
  ]);
  
  // 统计每个header出现的次数和值
  const headerCounts: Record<string, { count: number; values: Set<string> }> = {};
  for (const req of businessRequests) {
    for (const [name, value] of Object.entries(req.headers || {})) {
      const lowerName = name.toLowerCase();
      if (nonAuthHeaders.has(lowerName)) continue;
      if (lowerName.startsWith('sec-')) continue;
      
      if (!headerCounts[lowerName]) {
        headerCounts[lowerName] = { count: 0, values: new Set() };
      }
      headerCounts[lowerName].count++;
      headerCounts[lowerName].values.add(value);
    }
  }
  
  // v7.3.3: 阈值从 80% 降低到 50%，并增加值一致性检查
  // 认证 header 的特征：出现频率高 + 值一致（或只有少量不同值，如 token 刷新）
  const authHeaders: Record<string, { count: number; sampleValue: string }> = {};
  const threshold = businessRequests.length * 0.5;  // 50% 阈值
  
  for (const [name, data] of Object.entries(headerCounts)) {
    if (data.count >= threshold) {
      // 值一致性检查：认证 header 通常只有 1-2 个不同的值
      // 如果有太多不同值，说明是业务 header（如 request-id）
      if (data.values.size > 3) continue;
      
      // 排除已知的非认证header
      if (!nonAuthHeaders.has(name) && 
          !name.startsWith('x-gw-') &&  // 网关header
          name !== 'x-csrf-token' &&    // CSRF防护，不是认证
          name !== 'x-dlpj') {          // 先排除，后面单独处理
        authHeaders[name] = {
          count: data.count,
          sampleValue: maskValue([...data.values][0])
        };
      }
    }
  }
  
  // 单独检查可疑的自定义header（如 x-dlpj）
  for (const [name, data] of Object.entries(headerCounts)) {
    if (name.startsWith('x-') && !nonAuthHeaders.has(name) && 
        !name.startsWith('x-gw-') && name !== 'x-csrf-token' &&
        name !== 'x-requested-with' && data.count >= threshold &&
        data.values.size <= 3) {  // v7.3.3: 也检查值一致性
      if (!authHeaders[name]) {
        authHeaders[name] = {
          count: data.count,
          sampleValue: maskValue([...data.values][0])
        };
      }
    }
  }
  
  return authHeaders;
}

/**
 * 识别认证类型
 */
function identifyAuthType(authClues: Omit<AuthClues, 'authType'>): string {
  const types: string[] = [];
  
  // 检查URL参数
  if (authClues.urlAuthParams.length > 0) {
    types.push('url-ticket');
  }
  
  // 检查自定义header
  if (Object.keys(authClues.authHeaders).length > 0) {
    types.push('custom-header');
  }
  
  // 检查JWT
  if (authClues.authHeaders['authorization']) {
    types.push('jwt-bearer');
  }
  
  // 默认
  if (types.length === 0) {
    types.push('cookie-session');
  }
  
  return types.length === 1 ? types[0] : types.join(' + ');
}

/**
 * 收集认证线索（在页面内执行）
 */
async function collectAuthClues(page: Page, requests: CapturedRequest[]): Promise<AuthClues> {
  const url = page.url();
  
  // 1. URL参数中的认证信息
  const urlAuthParams = extractUrlAuthParams(url);
  
  // 2. 在页面内执行探测脚本
  let globalTokens: Record<string, string> = {};
  let storageTokens = { localStorage: {} as Record<string, string>, sessionStorage: {} as Record<string, string> };
  let cookies = '';
  
  try {
    const result = await page.evaluate(() => {
      const clues: any = {
        globalTokens: {} as Record<string, string>,
        storageTokens: { localStorage: {} as Record<string, string>, sessionStorage: {} as Record<string, string> },
        cookies: document.cookie
      };
      
      // 辅助函数：脱敏
      const mask = (v: any) => {
        if (!v || typeof v !== 'string') return String(v);
        if (v.length <= 8) return '***';
        return v.substring(0, 4) + '***' + v.substring(v.length - 4);
      };
      
      // 检查常见全局变量路径
      const globalPaths = [
        'pageConfig', '__TOKEN__', 'APP_CONFIG', 'appConfig', 
        'config', '__config__', 'auth', 'token', 'accessToken'
      ];
      
      for (const path of globalPaths) {
        try {
          const obj = (window as any)[path];
          if (obj) {
            if (typeof obj === 'string') {
              clues.globalTokens[path] = mask(obj);
            } else if (typeof obj === 'object') {
              for (const key of Object.keys(obj)) {
                const lowerKey = key.toLowerCase();
                if (lowerKey.includes('token') ||
                    lowerKey.includes('key') ||
                    lowerKey.includes('auth') ||
                    lowerKey.includes('session') ||
                    lowerKey.includes('ticket')) {
                  clues.globalTokens[`${path}.${key}`] = mask(obj[key]);
                }
              }
            }
          }
        } catch {}
      }
      
      // 检查localStorage
      try {
        for (let i = 0; i < localStorage.length; i++) {
          const key = localStorage.key(i);
          if (key) {
            const lowerKey = key.toLowerCase();
            if (lowerKey.includes('token') ||
                lowerKey.includes('auth') ||
                lowerKey.includes('session') ||
                lowerKey.includes('user')) {
              clues.storageTokens.localStorage[key] = mask(localStorage.getItem(key));
            }
          }
        }
      } catch {}
      
      // 检查sessionStorage
      try {
        for (let i = 0; i < sessionStorage.length; i++) {
          const key = sessionStorage.key(i);
          if (key) {
            const lowerKey = key.toLowerCase();
            if (lowerKey.includes('token') ||
                lowerKey.includes('auth') ||
                lowerKey.includes('session') ||
                lowerKey.includes('user')) {
              clues.storageTokens.sessionStorage[key] = mask(sessionStorage.getItem(key));
            }
          }
        }
      } catch {}
      
      return clues;
    });
    
    globalTokens = result.globalTokens;
    storageTokens = result.storageTokens;
    cookies = result.cookies;
  } catch {}
  
  // 3. 从请求中提取认证header
  const authHeaders = extractAuthHeaders(requests);
  
  // 4. 组装认证线索
  const clues: Omit<AuthClues, 'authType'> = {
    collectedAt: new Date().toISOString(),
    url,
    urlAuthParams,
    globalTokens,
    storageTokens,
    cookies,
    authHeaders
  };
  
  // 5. 识别认证类型
  const authType = identifyAuthType(clues);
  
  return { ...clues, authType };
}

// ─── Main ─────────────────────────────────────────────────────────────────────

program
  .name('record')
  .description('Record browser operations for web-autopilot automation')
  .requiredOption('-n, --name <name>', 'Task name (e.g. "提交报销单")')
  .option('-s, --sso-url <url>', 'SSO portal URL to open first')
  .option('-a, --app-url <url>', 'Directly open app URL (skip SSO)')
  .option('-o, --output <dir>', 'Output base directory', 'D:/Users/xubx4/.openclaw/rpa/tasks')
  .option('--viewport <WxH>', 'Browser window size', '1440x900')
  .option('--reuse <folder>', 'Reuse existing folder (for updating existing task)')
  .option('--save-full', 'Save full recording data (no filtering) - use this if you need complete data')
  .parse();

const opts = program.opts();

// 生成时间戳 YYYYMMDD_HHMM
function generateTimestamp(): string {
  const now = new Date();
  const y = now.getFullYear();
  const M = String(now.getMonth() + 1).padStart(2, '0');
  const d = String(now.getDate()).padStart(2, '0');
  const h = String(now.getHours()).padStart(2, '0');
  const m = String(now.getMinutes()).padStart(2, '0');
  return `${y}${M}${d}_${h}${m}`;
}

async function main() {
  const taskName: string = opts.name;
  const safeName = taskName.replace(/[^\w\u4e00-\u9fff-]/g, '_');
  
  // 文件夹命名：--reuse 复用已有文件夹，否则自动添加时间戳
  const folderName = opts.reuse || `${safeName}_${generateTimestamp()}`;
  const outputDir = path.join(opts.output, folderName);

  fs.mkdirSync(outputDir, { recursive: true });

  // v7.4.1: 创建 bodies 文件写入流（JSONL 格式，存所有响应体作为备份）
  const bodiesFilePath = path.join(outputDir, 'recording-bodies.jsonl');
  const bodiesStream = fs.createWriteStream(bodiesFilePath, { flags: 'w' });

  const startTime = Date.now();
  const requests: CapturedRequest[] = [];
  const responses: Record<string, CapturedResponse> = {};
  const actions: UserAction[] = [];
  const notes: string[] = [];
  const downloadEvents: DownloadEvent[] = [];  // v6.5: 下载事件列表

  const requestIndex = new WeakMap<Request, string>();
  let seqCounter = 0;

  console.log('\n╔════════════════════════════════════════════════════════════╗');
  console.log('║  🎬 web-autopilot v8.4.0 - Browser Recorder              ║');
  console.log('║  Author: 徐柏雄 (xubx4)                                    ║');
  console.log('║  反馈/交流：xubx4@midea.com | 13824820932                   ║');
  console.log('╚════════════════════════════════════════════════════════════╝');
  console.log(`\n    Task    : ${taskName}`);
  console.log(`    Output  : ${outputDir}\n`);

  const browser: Browser = await chromium.launch({ headless: false, channel: 'chrome', args: ['--start-maximized'] });
  const context: BrowserContext = await browser.newContext({ viewport: null, ignoreHTTPSErrors: true });

  // ── Inject enhanced action tracker BEFORE creating page (v6.7 fix) ─────────
  // 必须在 newPage() 之前调用 addInitScript，否则页面第一次加载（包括重定向）时脚本还没注入
  await context.addInitScript(() => {
    (window as any).__rpa_actions = [];
    (window as any).__rpa_validation_enabled = true;

    // ── v8.1.0: 混合策略全局变量 ──
    (window as any).__rpa_analysisQueue = [];  // 异步分析队列
    (window as any).__rpa_isProcessing = false; // 队列处理状态

    // ── v8.1.0: 混合策略 - 快照采集 + 快速验证 + 异步队列 ──

    // 同步快照采集（<0.5ms，只做 getAttribute/textContent，不做 querySelectorAll）
    function captureSnapshot(el: HTMLElement): any {
      const snapshot: any = {
        tag: el.tagName.toLowerCase(),
        id: el.id || null,
        text: el.textContent?.trim().substring(0, 80) || '',
        innerText: (el as any).innerText?.substring(0, 80) || '',
        attrs: {} as Record<string, string>,
        classes: Array.from(el.classList),
        ancestors: [] as any[],
        siblingsBefore: [] as any[],
        siblingsAfter: [] as any[],
      };

      // 收集所有属性（过滤无用属性）
      for (const attr of Array.from(el.attributes)) {
        const name = attr.name.toLowerCase();
        if (name.startsWith('on') || name === 'style') continue;
        if (name.startsWith('data-v-') || name.startsWith('data-reactid')) continue;
        snapshot.attrs[attr.name] = attr.value.substring(0, 200);
      }

      // 父级链（向上5层）
      let current: HTMLElement | null = el;
      for (let level = 0; level < 5 && current; level++) {
        const parent = current.parentElement;
        if (!parent) break;
        const siblings = Array.from(parent.children);
        snapshot.ancestors.push({
          tag: parent.tagName.toLowerCase(),
          id: parent.id || null,
          classes: Array.from(parent.classList).filter(c => isStableIdentifier(c)).slice(0, 3),
          text: parent.children.length === 0 ? (parent.textContent?.trim().substring(0, 50) || '') : '',
          childIndex: siblings.indexOf(current),
          siblingCount: siblings.length,
        });
        current = parent;
      }

      // 兄弟节点（前后各3个）
      const parent = el.parentElement;
      if (parent) {
        const siblings = Array.from(parent.children);
        const myIndex = siblings.indexOf(el);
        for (let i = Math.max(0, myIndex - 3); i < myIndex; i++) {
          const sib = siblings[i] as HTMLElement;
          snapshot.siblingsBefore.push({
            tag: sib.tagName.toLowerCase(),
            text: sib.textContent?.trim().substring(0, 30) || '',
            distance: myIndex - i,
          });
        }
        for (let i = myIndex + 1; i < Math.min(siblings.length, myIndex + 4); i++) {
          const sib = siblings[i] as HTMLElement;
          snapshot.siblingsAfter.push({
            tag: sib.tagName.toLowerCase(),
            text: sib.textContent?.trim().substring(0, 30) || '',
            distance: i - myIndex,
          });
        }
      }

      return snapshot;
    }

    // 同步快速验证（<1.5ms，只检查top 5候选）
    function quickValidation(el: HTMLElement, snapshot: any): { found: boolean; selector?: string; grade?: string; matchCount?: number; strategy?: string; candidates?: any[] } {
      const quickCandidates: Array<{ sel: string; grade: string; source: string }> = [];

      // 1. 稳定ID
      if (snapshot.id && isStableIdentifier(snapshot.id)) {
        quickCandidates.push({ sel: `#${snapshot.id}`, grade: 'S', source: 'stable-id' });
      }

      // 2. data属性（最多取3个）
      let dataCount = 0;
      for (const [key, value] of Object.entries(snapshot.attrs)) {
        if (key.startsWith('data-') && isStableIdentifier(value as string)) {
          quickCandidates.push({ sel: `[${key}="${value}"]`, grade: 'S', source: `attr:${key}` });
          dataCount++;
          if (dataCount >= 3) break;
        }
      }

      // 3. 文本定位
      if (snapshot.text && snapshot.text.length > 0 && snapshot.text.length <= 30 && isStableIdentifier(snapshot.text)) {
        quickCandidates.push({ sel: `${snapshot.tag}:has-text("${snapshot.text.replace(/["\\]/g, '\\$&')}")`, grade: 'A', source: 'text' });
      }

      // 4. 属性组合（type/placeholder/name/aria-label/role）
      const attrParts: string[] = [];
      if (snapshot.attrs['type']) attrParts.push(`[type="${snapshot.attrs['type']}"]`);
      if (snapshot.attrs['placeholder']) attrParts.push(`[placeholder="${snapshot.attrs['placeholder']}"]`);
      if (snapshot.attrs['name'] && isStableIdentifier(snapshot.attrs['name'])) attrParts.push(`[name="${snapshot.attrs['name']}"]`);
      if (snapshot.attrs['aria-label']) attrParts.push(`[aria-label="${snapshot.attrs['aria-label']}"]`);
      if (snapshot.attrs['role']) attrParts.push(`[role="${snapshot.attrs['role']}"]`);
      if (attrParts.length >= 2) {
        quickCandidates.push({ sel: `${snapshot.tag}${attrParts.join('')}`, grade: 'A', source: 'attrs-combined' });
      }

      // 5. name 属性（单独）
      if (snapshot.attrs['name'] && isStableIdentifier(snapshot.attrs['name']) && attrParts.length < 2) {
        quickCandidates.push({ sel: `[name="${snapshot.attrs['name']}"]`, grade: 'S', source: 'name' });
      }

      // 快速验证每个候选（最多5个）
      const allCandidates: any[] = [];
      for (const cand of quickCandidates.slice(0, 5)) {
        try {
          let matchCount = 0;
          if (cand.sel.includes(':has-text')) {
            const tag = cand.sel.split(':')[0];
            const textMatch = cand.sel.match(/:has-text\("(.+?)"\)/);
            if (textMatch) {
              matchCount = countElementsWithText(tag, textMatch[1]);
            }
          } else {
            matchCount = document.querySelectorAll(cand.sel).length;
          }
          const confidence = matchCount === 1 ? 0.95 : matchCount <= 5 ? 0.6 : 0.2;
          allCandidates.push({
            selector: cand.sel,
            grade: cand.grade,
            matchCount,
            strategy: cand.source,
            confidence,
          });
          if (matchCount === 1) {
            return { found: true, selector: cand.sel, grade: cand.grade, matchCount: 1, strategy: cand.source, candidates: allCandidates };
          }
        } catch {}
      }

      return { found: false, candidates: allCandidates };
    }

    // 异步队列调度
    function scheduleSelectorAnalysis(actionIndex: number, snapshot: any) {
      (window as any).__rpa_analysisQueue.push({ actionIndex, snapshot, timestamp: Date.now() });
      if (!(window as any).__rpa_isProcessing) {
        (window as any).__rpa_isProcessing = true;
        const schedule = (window as any).requestIdleCallback || ((cb: Function) => setTimeout(cb, 0));
        schedule(processAnalysisQueue);
      }
    }

    // 异步处理队列
    function processAnalysisQueue(deadline?: { timeRemaining: () => number }) {
      const queue = (window as any).__rpa_analysisQueue;
      const timeBudget = deadline ? deadline.timeRemaining() : 10;

      while (queue.length > 0 && timeBudget > 2) {
        const item = queue.shift();
        const action = (window as any).__rpa_actions[item.actionIndex];
        if (!action) continue;

        // 基于快照生成完整候选列表
        const candidates = analyzeFromSnapshot(item.snapshot);

        // 选最佳候选
        const best = candidates[0];
        if (best && action.selectorStrategy === 'pending') {
          action.target = best.selector;
          action.stabilityGrade = best.grade;
          action.uniquenessMatch = best.matchCount;
          action.selectorStrategy = best.strategy;
          action.confidence = best.confidence;
          action.candidates = candidates;
        }
      }

      if (queue.length > 0) {
        const schedule = (window as any).requestIdleCallback || ((cb: Function) => setTimeout(cb, 0));
        schedule(processAnalysisQueue);
      } else {
        (window as any).__rpa_isProcessing = false;
      }
    }

    // 基于快照生成完整候选选择器列表
    function analyzeFromSnapshot(snapshot: any): any[] {
      const candidates: any[] = [];

      // S1: 稳定ID
      if (snapshot.id && isStableIdentifier(snapshot.id)) {
        candidates.push({ selector: `#${snapshot.id}`, grade: 'S', matchCount: 1, strategy: 'stable-id', confidence: 0.95 });
      }

      // S2: data属性
      for (const [key, value] of Object.entries(snapshot.attrs)) {
        if (key.startsWith('data-') && isStableIdentifier(value as string)) {
          candidates.push({ selector: `[${key}="${value}"]`, grade: 'S', matchCount: 1, strategy: `attr:${key}`, confidence: 0.90 });
        }
      }

      // S3: 文本定位
      if (snapshot.text && snapshot.text.length > 0 && snapshot.text.length <= 30 && isStableIdentifier(snapshot.text)) {
        const escapedText = snapshot.text.replace(/["\\]/g, '\\$&');
        candidates.push({ selector: `${snapshot.tag}:has-text("${escapedText}")`, grade: 'A', matchCount: -1, strategy: 'text+snapshot', confidence: 0.80 });
      }

      // S4: 属性组合
      const attrParts: string[] = [];
      if (snapshot.attrs['type']) attrParts.push(`[type="${snapshot.attrs['type']}"]`);
      if (snapshot.attrs['placeholder']) attrParts.push(`[placeholder="${snapshot.attrs['placeholder']}"]`);
      if (snapshot.attrs['name'] && isStableIdentifier(snapshot.attrs['name'])) attrParts.push(`[name="${snapshot.attrs['name']}"]`);
      if (snapshot.attrs['aria-label']) attrParts.push(`[aria-label="${snapshot.attrs['aria-label']}"]`);
      if (attrParts.length >= 2) {
        candidates.push({ selector: `${snapshot.tag}${attrParts.join('')}`, grade: 'A', matchCount: -1, strategy: 'attrs-combined+snapshot', confidence: 0.75 });
      }

      // S5: 父级ID + 当前元素
      for (const ancestor of snapshot.ancestors) {
        if (ancestor.id && isStableIdentifier(ancestor.id)) {
          const attrSel = attrParts.length > 0 ? attrParts.join('') : '';
          candidates.push({ selector: `#${ancestor.id} ${snapshot.tag}${attrSel}`, grade: 'A', matchCount: -1, strategy: 'ancestor-id+attrs', confidence: 0.70 });
          if (snapshot.text && snapshot.text.length <= 30 && isStableIdentifier(snapshot.text)) {
            const escapedText = snapshot.text.replace(/["\\]/g, '\\$&');
            candidates.push({ selector: `#${ancestor.id} ${snapshot.tag}:has-text("${escapedText}")`, grade: 'A', matchCount: -1, strategy: 'ancestor-id+text', confidence: 0.65 });
          }
          break;
        }
      }

      // S6: 兄弟文本定位
      if (snapshot.siblingsBefore && snapshot.siblingsBefore.length > 0) {
        const nearest = snapshot.siblingsBefore[0];
        if (nearest.text && nearest.text.length > 0 && nearest.text.length <= 30 && isStableIdentifier(nearest.text)) {
          const escapedSibText = nearest.text.replace(/["\\]/g, '\\$&');
          candidates.push({ selector: `${nearest.tag}:has-text("${escapedSibText}") + ${snapshot.tag}`, grade: 'A', matchCount: -1, strategy: 'sibling-text+snapshot', confidence: 0.60 });
        }
      }

      // S7: 位置兜底
      if (snapshot.ancestors.length > 0) {
        const parent = snapshot.ancestors[0];
        const parentSel = parent.id ? `#${parent.id}` :
                          parent.classes.length > 0 ? `.${parent.classes[0]}` : parent.tag;
        candidates.push({ selector: `${parentSel} > ${snapshot.tag}:nth-child(${parent.childIndex + 1})`, grade: 'B', matchCount: -1, strategy: 'parent+nth+snapshot', confidence: 0.40 });
      }

      // 按 confidence 排序
      candidates.sort((a, b) => b.confidence - a.confidence);
      return candidates;
    }

    // 强制处理完队列（录制完成时调用）
    function flushAnalysisQueue() {
      const queue = (window as any).__rpa_analysisQueue;
      while (queue.length > 0) {
        const item = queue.shift();
        const action = (window as any).__rpa_actions[item.actionIndex];
        if (!action) continue;
        const candidates = analyzeFromSnapshot(item.snapshot);
        const best = candidates[0];
        if (best && (action.selectorStrategy === 'pending' || !action.selectorStrategy)) {
          action.target = best.selector;
          action.stabilityGrade = best.grade;
          action.uniquenessMatch = best.matchCount;
          action.selectorStrategy = best.strategy;
          action.confidence = best.confidence;
          action.candidates = candidates;
        }
      }
      // 清理所有 pending 状态
      for (const action of (window as any).__rpa_actions) {
        if (action.selectorStrategy === 'pending') {
          action.selectorStrategy = 'snapshot-fallback';
          action.stabilityGrade = 'C';
          action.confidence = 0.3;
        }
      }
    }

    // ── Selector stability classification ──
    function classifyStability(selector: string): 'S' | 'A' | 'B' | 'C' | 'D' {
      if (!selector || selector === 'unknown') return 'D';
      // S: stable id (not dynamic), data-testid, name
      if (/^#[a-zA-Z][\w-]*$/.test(selector) && !/__\w+__\d+/.test(selector) && !/_[0-9a-f]{5,}/.test(selector)) return 'S';
      if (/\[data-testid=/.test(selector)) return 'S';
      if (/\[name=/.test(selector)) return 'S';
      // A: aria-label, text-based, placeholder
      if (/\[aria-label=/.test(selector)) return 'A';
      if (/:has-text\(|:text\(/.test(selector)) return 'A';
      if (/\[placeholder=/.test(selector)) return 'A';
      // C: contains dynamic-looking class/id patterns
      if (/[a-z]{3,}[-_][a-z0-9]{5,}/i.test(selector)) return 'C';  // styled-components, CSS modules
      if (/[0-9a-f]{6,}/.test(selector)) return 'C';                  // hash patterns
      if (/data-v-|data-reactid/.test(selector)) return 'C';          // Vue/React internal
      // B: role, structure, attribute combinations
      if (/\[role=/.test(selector)) return 'B';
      if (/>|~|\+|:nth-/.test(selector)) return 'B';
      // D: pure tag+random class
      if (/^\w+\.[\w-]+$/.test(selector) && /[-_]\w{4,}$/.test(selector)) return 'D';
      return 'B';  // default to B if uncertain
    }

    // ── Check if an identifier is stable (not random/dynamic) ──
    function isStableIdentifier(str: string): boolean {
      if (!str) return false;
      // Reject: hash patterns (6+ hex chars) but allow business IDs like "100909"
      // Only reject if it looks like a hex hash (contains a-f)
      if (/[a-f][0-9a-f]{5,}/i.test(str) && /[a-f]/i.test(str)) return false;
      // Reject: styled-components patterns (sc-xxx, css-xxx)
      if (/^(sc|css|css-module)-[a-z]{3,}/i.test(str)) return false;
      // Reject: Vue/React internal attributes
      if (/data-v-|data-reactid|__\w+__\d+/.test(str)) return false;
      // Reject: very short random-looking classes (3 chars or less with numbers)
      if (/^[a-z]{0,2}[0-9][a-z0-9]{0,2}$/i.test(str)) return false;
      return true;
    }

    // ── Check if element text matches (native JS, no :has-text) ──
    // Used for validation since querySelectorAll doesn't support :has-text
    function elementMatchesText(el: Element, text: string): boolean {
      const elText = el.textContent?.trim() || '';
      return elText === text || elText.includes(text);
    }

    // ── Count elements matching text (native JS implementation) ──
    function countElementsWithText(tag: string, text: string, scope: Element | Document = document): number {
      const elements = scope.querySelectorAll(tag);
      let count = 0;
      elements.forEach(el => {
        if (elementMatchesText(el, text)) count++;
      });
      return count;
    }

    // ── Find element with text in siblings ──
    function findSiblingWithText(el: Element, text: string): Element | null {
      const parent = el.parentElement;
      if (!parent) return null;
      const siblings = Array.from(parent.children);
      return siblings.find(sib => sib !== el && elementMatchesText(sib, text)) || null;
    }

    // ── Generate selector with stability info ──
    function genSelector(el: Element): { raw: string; grade: 'S' | 'A' | 'B' | 'C' | 'D' } {
      if (!el || el.nodeType !== 1) return { raw: 'unknown', grade: 'D' };
      const e = el as HTMLElement;
      let raw = 'unknown';
      
      // Special handling for SVG elements
      // Fix: Always try ancestor ID first, because SVG class (like "svg-icon") is usually not unique
      if (e.tagName.toLowerCase() === 'svg' || e instanceof SVGElement) {
        const svgClass = e.getAttribute('class');
        const svgClassPart = svgClass && isStableIdentifier(svgClass.split(' ')[0]) 
          ? `.${svgClass.split(' ')[0]}` 
          : '';
        
        // Priority 1: Find ancestor with stable ID (most reliable for SVG)
        let ancestor: HTMLElement | null = e.parentElement;
        for (let i = 0; i < 10 && ancestor; i++) {
          if (ancestor.id && isStableIdentifier(ancestor.id)) {
            raw = `#${ancestor.id} svg${svgClassPart}`;
            return { raw, grade: classifyStability(raw) };
          }
          ancestor = ancestor.parentElement;
        }
        
        // Priority 2: Try parent wrapper class
        const parentWrapper = e.closest('.card-menu-wrapper, .card-header-tail, [class*="menu"], [class*="icon"]');
        if (parentWrapper) {
          const wrapperClass = Array.from(parentWrapper.classList)
            .filter(c => isStableIdentifier(c))
            .slice(0, 2)
            .join('.');
          if (wrapperClass) {
            raw = `.${wrapperClass} svg`;
            return { raw, grade: classifyStability(raw) };
          }
        }
        
        // Priority 3: Use SVG class alone (last resort)
        if (svgClassPart) {
          raw = `svg${svgClassPart}`;
        } else {
          raw = 'svg';
        }
        return { raw, grade: classifyStability(raw) };
      }
      
      if (e.id && !/__\w+__\d+/.test(e.id) && !/_[0-9a-f]{5,}/.test(e.id)) {
        raw = `#${e.id}`;
      } else {
        const testId = e.getAttribute('data-testid') || e.getAttribute('data-test-id');
        if (testId) raw = `[data-testid="${testId}"]`;
        else if (e.getAttribute('name')) raw = `[name="${e.getAttribute('name')}"]`;
        else if (e.getAttribute('aria-label')) raw = `[aria-label="${e.getAttribute('aria-label')!.substring(0, 40)}"]`;
        else {
          // v7.5.0: 增加 selected|current|open|closed 过滤，覆盖更多状态类命名
          const classes = Array.from(e.classList).filter(c => !/^(hover|focus|active|is-|has-|ng-|v-|state-|mod-|selected|current|open|closed)/.test(c)).slice(0, 2);
          raw = e.tagName.toLowerCase() + (classes.length ? '.' + classes.join('.') : '');
        }
      }
      return { raw, grade: classifyStability(raw) };
    }

    // ── Build enhanced selector when base is not unique ──
    // Returns: { selector, grade, matchCount, strategy }
    function buildUniqueSelector(el: HTMLElement): { 
      selector: string; 
      grade: 'S' | 'A' | 'B' | 'C' | 'D'; 
      matchCount: number;
      strategy: string;
    } {
      // Guard: element must be connected to DOM and have a valid tagName
      if (!el || !el.tagName || !document.contains(el)) {
        return { selector: 'unknown', grade: 'D', matchCount: 0, strategy: 'disconnected' };
      }
      try {
      return _buildUniqueSelectorInner(el);
      } catch (err) {
        return { selector: 'unknown', grade: 'D', matchCount: 0, strategy: 'error' };
      }
    }
    function _buildUniqueSelectorInner(el: HTMLElement): { 
      selector: string; 
      grade: 'S' | 'A' | 'B' | 'C' | 'D'; 
      matchCount: number;
      strategy: string;
    } {
      const tag = el.tagName.toLowerCase();
      
      // ========== 第一步：收集所有可用属性，后续策略融合使用 ==========
      const attrParts: string[] = [];
      const collectedAttrs: { type?: string; placeholder?: string; name?: string; ariaLabel?: string; role?: string } = {};
      
      // 收集稳定属性
      const type = el.getAttribute('type');
      const placeholder = el.getAttribute('placeholder');
      const name = el.getAttribute('name');
      const ariaLabel = el.getAttribute('aria-label');
      const role = el.getAttribute('role');
      const dataTestId = el.getAttribute('data-testid');
      
      if (type && isStableIdentifier(type)) {
        attrParts.push(`[type="${type}"]`);
        collectedAttrs.type = type;
      }
      if (placeholder && isStableIdentifier(placeholder)) {
        attrParts.push(`[placeholder="${placeholder}"]`);
        collectedAttrs.placeholder = placeholder;
      }
      if (name && isStableIdentifier(name) && !dataTestId) { // name 已被 stable-id 处理，避免重复
        attrParts.push(`[name="${name}"]`);
        collectedAttrs.name = name;
      }
      if (ariaLabel && isStableIdentifier(ariaLabel)) {
        attrParts.push(`[aria-label="${ariaLabel}"]`);
        collectedAttrs.ariaLabel = ariaLabel;
      }
      if (role && isStableIdentifier(role)) {
        attrParts.push(`[role="${role}"]`);
        collectedAttrs.role = role;
      }
      
      // 带所有属性的 tag 选择器（后续策略融合使用）
      const tagWithAttrs = `${tag}${attrParts.join('')}`;
      
      // 获取元素文本内容（后续策略融合使用）
      const textContent = el.textContent?.trim() || '';
      const hasStableText = textContent.length > 0 && textContent.length <= 30 && isStableIdentifier(textContent);
      const escapedText = hasStableText ? textContent.replace(/["\\]/g, '\\$&') : '';
      
      // Strategy 1: Use stable attributes first (id, data-testid, name)
      const { raw: baseSel, grade: baseGrade } = genSelector(el);
      if (baseGrade === 'S') {
        const matches = document.querySelectorAll(baseSel);
        if (matches.length === 1) {
          return { selector: baseSel, grade: 'S', matchCount: 1, strategy: 'stable-id' };
        }
      }

      // Strategy 2: 使用融合属性的选择器（比原来更精确）
      if (attrParts.length > 0) {
        const sel = tagWithAttrs;
        const matches = document.querySelectorAll(sel);
        if (matches.length === 1) {
          return { selector: sel, grade: 'A', matchCount: 1, strategy: 'attrs-combined' };
        }
      }

      // Strategy 2.5: Associate input with related label/text（融合属性）
      if (tag === 'input' || tag === 'select' || tag === 'textarea') {
        // Method 1: aria-labelledby or aria-describedby
        const ariaLabelledBy = el.getAttribute('aria-labelledby') || el.getAttribute('aria-describedby');
        if (ariaLabelledBy) {
          const labelEl = document.getElementById(ariaLabelledBy);
          if (labelEl) {
            const labelText = labelEl.textContent?.trim() || '';
            if (labelText.length > 0 && labelText.length <= 30 && isStableIdentifier(labelText)) {
              const labelParent = labelEl.closest('[id]');
              if (labelParent && labelParent.id && isStableIdentifier(labelParent.id)) {
                // 融合：父级ID + 带属性的 tag
                const sel = `#${labelParent.id} ${tagWithAttrs}`;
                const matches = document.querySelectorAll(sel);
                if (matches.length === 1) {
                  return { selector: sel, grade: 'A', matchCount: 1, strategy: 'aria-label+attrs' };
                }
              }
            }
          }
        }
        
        // Method 2: Find nearest text node in ancestor chain（融合属性）
        let searchEl: HTMLElement | null = el;
        for (let level = 0; level < 5 && searchEl; level++) {
          const parent = searchEl.parentElement;
          if (!parent) break;
          
          const textChildren = Array.from(parent.children).filter(child => {
            if (child === el) return false;
            const childText = child.textContent?.trim() || '';
            return childText.length > 0 && childText.length <= 30 && isStableIdentifier(childText);
          });
          
          if (textChildren.length === 1) {
            const labelChild = textChildren[0] as HTMLElement;
            const labelText = labelChild.textContent?.trim() || '';
            
            const parentTag = parent.tagName.toLowerCase();
            const parentClass = Array.from(parent.classList).filter(c => isStableIdentifier(c)).slice(0, 2).join('.');
            const parentSel = parentClass ? `${parentTag}.${parentClass}` : parentTag;
            
            const parentMatches = document.querySelectorAll(parentSel);
            if (parentMatches.length === 1) {
              // 融合：父级选择器 + 带属性的 tag
              const sel = `${parentSel} ${tagWithAttrs}`;
              const matches = document.querySelectorAll(sel);
              if (matches.length === 1) {
                return { selector: sel, grade: 'A', matchCount: 1, strategy: 'label+attrs' };
              }
            }
          }
          
          searchEl = parent;
        }
      }

      // Strategy 3: 文本内容 + 融合属性
      if (hasStableText) {
        // 尝试：tag:has-text + 属性
        const selWithTextAndAttrs = `${tagWithAttrs}:has-text("${escapedText}")`;
        const matchCount = countElementsWithText(tag, textContent);
        if (matchCount === 1) {
          return { selector: selWithTextAndAttrs, grade: 'A', matchCount: 1, strategy: 'text+attrs' };
        }
        
        // Strategy 3.5: Text + position combination（融合属性）
        if (matchCount > 1 && matchCount <= 50) {
          let searchEl: HTMLElement | null = el;
          for (let level = 0; level < 10 && searchEl; level++) {
            const parent = searchEl.parentElement;
            if (!parent) break;
            
            if (parent.id && isStableIdentifier(parent.id)) {
              const siblings = Array.from(parent.children).filter(c => c.tagName === el.tagName);
              const index = siblings.indexOf(el) + 1;
              
              if (index > 0) {
                // 融合：父级ID + 带属性的 tag + 文本 + 位置
                const sel = `#${parent.id} ${tagWithAttrs}:has-text("${escapedText}"):nth-of-type(${index})`;
                const matches = document.querySelectorAll(sel);
                if (matches.length === 1) {
                  return { selector: sel, grade: 'A', matchCount: 1, strategy: 'parent+text+attrs+pos' };
                }
              }
            }
            
            searchEl = parent;
          }
          
          // 直接父级 + 位置
          const directParent = el.parentElement;
          if (directParent) {
            const sameTagSiblings = Array.from(directParent.children).filter(c => c.tagName === el.tagName);
            if (sameTagSiblings.length > 1) {
              const index = sameTagSiblings.indexOf(el) + 1;
              const parentTag = directParent.tagName.toLowerCase();
              const parentClass = Array.from(directParent.classList).filter(c => isStableIdentifier(c)).slice(0, 2).join('.');
              const parentSel = parentClass ? `${parentTag}.${parentClass}` : parentTag;
              
              // 融合：父级 + 带属性的 tag + 文本 + 位置
              const sel = `${parentSel} > ${tagWithAttrs}:has-text("${escapedText}"):nth-of-type(${index})`;
              const matches = document.querySelectorAll(sel);
              if (matches.length === 1) {
                return { selector: sel, grade: 'A', matchCount: 1, strategy: 'parent+text+attrs+nth' };
              }
            }
          }
        }
      }

      // Strategy 4: 父级限定 + 融合属性
      let currentEl: HTMLElement | null = el;
      for (let level = 0; level < 10 && currentEl; level++) {
        const parent = currentEl.parentElement;
        if (!parent) break;
        
        const parentId = parent.id;
        const parentTestId = parent.getAttribute('data-testid');
        const parentName = parent.getAttribute('name');
        
        let parentPrefix = '';
        if (parentId && isStableIdentifier(parentId)) {
          parentPrefix = `#${parentId}`;
        } else if (parentTestId && isStableIdentifier(parentTestId)) {
          parentPrefix = `[data-testid="${parentTestId}"]`;
        } else if (parentName && isStableIdentifier(parentName)) {
          parentPrefix = `[name="${parentName}"]`;
        }
        
        if (parentPrefix) {
          // 融合：父级 + 带属性的 tag
          const combinedSel = `${parentPrefix} ${tagWithAttrs}`;
          const matches = document.querySelectorAll(combinedSel);
          if (matches.length === 1) {
            return { selector: combinedSel, grade: 'A', matchCount: 1, strategy: `parent+attrs-${level}` };
          }
          
          // 融合：父级 + 带属性的 tag + 文本
          if (hasStableText) {
            const parentMatches = document.querySelectorAll(parentPrefix);
            if (parentMatches.length === 1) {
              const textMatchCount = countElementsWithText(tag, textContent, parentMatches[0]);
              if (textMatchCount === 1) {
                const combinedTextSel = `${parentPrefix} ${tagWithAttrs}:has-text("${escapedText}")`;
                return { selector: combinedTextSel, grade: 'A', matchCount: 1, strategy: `parent+text+attrs-${level}` };
              }
            }
          }
        }
        
        currentEl = parent;
      }

      // Strategy 5: Add class-based qualifier（融合属性）
      const stableClasses = Array.from(el.classList).filter(c => isStableIdentifier(c));
      if (stableClasses.length > 0) {
        // 融合：tag + class + 属性
        const classWithAttrs = `${tag}.${stableClasses.slice(0, 3).join('.')}${attrParts.join('')}`;
        const matches = document.querySelectorAll(classWithAttrs);
        if (matches.length === 1) {
          return { selector: classWithAttrs, grade: 'B', matchCount: 1, strategy: 'stable-classes+attrs' };
        }
      }

      // Strategy 5.5: Relative positioning via stable siblings（融合属性）
      const parent = el.parentElement;
      if (parent) {
        const siblings = Array.from(parent.children);
        const targetIndex = siblings.indexOf(el);
        
        // 向前查找稳定参考元素（左边的兄弟）
        for (let i = targetIndex - 1; i >= 0; i--) {
          const sibling = siblings[i] as HTMLElement;
          const { raw: sibSel, grade: sibGrade } = genSelector(sibling);
          
          if (sibGrade === 'S' || sibGrade === 'A') {
            // 融合：兄弟 + 带属性的 tag
            if (i === targetIndex - 1) {
              const adjacentSel = `${sibSel} + ${tagWithAttrs}`;
              const matches = document.querySelectorAll(adjacentSel);
              if (matches.length === 1) {
                return { selector: adjacentSel, grade: 'A', matchCount: 1, strategy: 'sibling-adjacent+attrs' };
              }
            }
            
            const generalSel = `${sibSel} ~ ${tagWithAttrs}`;
            const matches = document.querySelectorAll(generalSel);
            if (matches.length === 1) {
              return { selector: generalSel, grade: 'A', matchCount: 1, strategy: 'sibling-general+attrs' };
            }
          }
          
          // 兄弟文本 + 带属性的 tag
          const sibText = sibling.textContent?.trim() || '';
          if (sibText.length > 0 && sibText.length <= 30 && isStableIdentifier(sibText)) {
            const siblingTextCount = siblings.filter(s => {
              const sText = s.textContent?.trim() || '';
              return sText === sibText || sText.includes(sibText);
            }).length;
            
            if (siblingTextCount === 1) {
              const escapedSibText = sibText.replace(/["\\]/g, '\\$&');
              const sibTextSel = `${sibling.tagName.toLowerCase()}:has-text("${escapedSibText}")`;
              
              if (i === targetIndex - 1) {
                const adjacentSel = `${sibTextSel} + ${tagWithAttrs}`;
                const prevSibling = siblings[targetIndex - 1];
                if (prevSibling && elementMatchesText(prevSibling, sibText)) {
                  return { selector: adjacentSel, grade: 'A', matchCount: 1, strategy: 'sibling-text-adjacent+attrs' };
                }
              }
              
              const generalSel = `${sibTextSel} ~ ${tagWithAttrs}`;
              const targetAfterSibling = siblings.slice(i + 1).includes(el);
              if (targetAfterSibling) {
                return { selector: generalSel, grade: 'A', matchCount: 1, strategy: 'sibling-text-general+attrs' };
              }
            }
          }
          
          if (targetIndex - i > 3) break;
        }
        
        // 向后查找稳定参考元素
        for (let i = targetIndex + 1; i < siblings.length; i++) {
          const sibling = siblings[i] as HTMLElement;
          const { raw: sibSel, grade: sibGrade } = genSelector(sibling);
          
          if (sibGrade === 'S' || sibGrade === 'A') {
            const parentSel = genSelector(parent).raw;
            if (parentSel && parentSel !== 'unknown') {
              // 融合：父级 + 带属性的 tag + nth-child
              const nthSel = `${parentSel} > ${tagWithAttrs}:nth-child(${targetIndex + 1})`;
              const matches = document.querySelectorAll(nthSel);
              if (matches.length === 1) {
                return { selector: nthSel, grade: 'B', matchCount: 1, strategy: 'nth-child-with-stable-parent+attrs' };
              }
            }
          }
          
          if (i - targetIndex > 3) break;
        }
        
        // Strategy 5.6: Uncle-level text search（融合属性）
        const grandparent = parent.parentElement;
        if (grandparent) {
          const uncles = Array.from(grandparent.children).filter(c => c !== parent);
          const parentIndex = Array.from(grandparent.children).indexOf(parent);
          
          for (const uncle of uncles) {
            const uncleText = uncle.textContent?.trim() || '';
            if (uncleText.length > 0 && uncleText.length <= 30 && isStableIdentifier(uncleText)) {
              const uncleTextCount = uncles.filter(u => {
                const uText = u.textContent?.trim() || '';
                return uText === uncleText;
              }).length;
              
              if (uncleTextCount === 1) {
                const uncleIndex = Array.from(grandparent.children).indexOf(uncle);
                if (uncleIndex >= parentIndex) continue;
                
                const escapedUncleText = uncleText.replace(/["\\]/g, '\\$&');
                const uncleTag = uncle.tagName.toLowerCase();
                const uncleTextSel = `${uncleTag}:has-text("${escapedUncleText}")`;
                
                const parentTag = parent.tagName.toLowerCase();
                const parentClass = Array.from(parent.classList).filter(c => isStableIdentifier(c)).slice(0, 2).join('.');
                const parentSel = parentClass ? `${parentTag}.${parentClass}` : parentTag;
                
                // 融合：uncle + parent + 带属性的 tag
                const generalSel = `${uncleTextSel} ~ ${parentSel} > ${tagWithAttrs}`;
                const matches = document.querySelectorAll(generalSel);
                if (matches.length === 1) {
                  return { selector: generalSel, grade: 'A', matchCount: 1, strategy: 'uncle-text+attrs' };
                }
                
                const adjacentSel = `${uncleTextSel} + ${parentSel} > ${tagWithAttrs}`;
                const adjMatches = document.querySelectorAll(adjacentSel);
                if (adjMatches.length === 1) {
                  return { selector: adjacentSel, grade: 'A', matchCount: 1, strategy: 'uncle-text-adjacent+attrs' };
                }
              }
            }
          }
        }
      }

      // Strategy 6: Use position as last resort（融合属性）
      if (parent) {
        const siblings = Array.from(parent.children).filter(c => c.tagName === el.tagName);
        if (siblings.length > 1) {
          const index = siblings.indexOf(el) + 1;
          // 融合：带属性的 tag + nth-of-type
          const nthSel = `${tagWithAttrs}:nth-of-type(${index})`;
          const matches = document.querySelectorAll(nthSel);
          if (matches.length === 1) {
            return { selector: nthSel, grade: 'B', matchCount: 1, strategy: 'nth-of-type+attrs' };
          }
        }
      }

      // Fallback: return tagWithAttrs with match count
      const finalMatches = document.querySelectorAll(tagWithAttrs);
      return { 
        selector: tagWithAttrs, 
        grade: finalMatches.length === 1 ? 'A' : (finalMatches.length <= 5 ? 'B' : 'C'), 
        matchCount: finalMatches.length, 
        strategy: 'fallback+attrs' 
      };
    }

    // ── Sensitive field detection ──
    function isSensitiveField(el: HTMLElement): boolean {
      const name = (el.getAttribute('name') || '').toLowerCase();
      const id = (el.id || '').toLowerCase();
      const placeholder = (el.getAttribute('placeholder') || '').toLowerCase();
      const type = (el as HTMLInputElement).type?.toLowerCase() || '';
      const sensitivePatterns = [
        /password|passwd|pwd/,
        /id_?card|身份证|identity/,
        /bank_?card|银行卡|credit_?card/,
        /phone|手机|mobile|tel/,
        /ssn|social_?security/,
        /cvv|cvc|csv/,
      ];
      if (type === 'password') return true;
      return sensitivePatterns.some(p => p.test(name) || p.test(id) || p.test(placeholder));
    }

    // ── Event listeners with isTrusted check ──
    // v8.1.0: 混合策略 - 快照 + 快速验证 → 命中则跳过 buildUniqueSelector
    document.addEventListener('click', (e: MouseEvent) => {
      if (!e.isTrusted) return;  // Filter synthetic events
      const target = e.composedPath()[0] as HTMLElement;
      if (!target) return;
      const now = Date.now();

      // ── v8.1.0 混合策略 ──
      const snapshot = captureSnapshot(target);
      const quick = quickValidation(target, snapshot);
      let selector: string;
      let grade: string;
      let matchCount: number;
      let strategy: string;
      let candidates: any[] | undefined;

      if (quick.found) {
        // 快速验证命中 → 跳过 buildUniqueSelector，节省 5~20ms
        selector = quick.selector!;
        grade = quick.grade!;
        matchCount = quick.matchCount!;
        strategy = quick.strategy!;
        candidates = quick.candidates;
      } else {
        // 快速验证未命中 → 走完整策略链（元素还在DOM中，结果最准确）
        const result = buildUniqueSelector(target);
        selector = result.selector;
        grade = result.grade;
        matchCount = result.matchCount;
        strategy = result.strategy;
        candidates = quick.candidates; // 保留快速验证阶段的候选
      }
      
      // Fix #3: Enhance selector with recent hover context
      // If the click selector is low-quality (fallback/C/D grade) and there was a recent
      // significant hover (with stable ID), use the hover's selector as parent qualifier
      const recentHover = (window as any).__rpa_lastSignificantHover;
      if (recentHover && recentHover.stableId && (now - recentHover.timestamp) < 5000) {
        // Check if the click target is inside the hovered element's ancestor
        const hoveredEl = target.closest(recentHover.stableId);
        if (hoveredEl) {
          // v7.2 fix: 拼接前先去除 click selector 中已有的祖先 ID 前缀，避免重复
          // 例：click selector = "#qbi-zz1z0ieo svg.svg-icon"，hover stableId = "#qbi-zz1z0ieo"
          // 错误拼法：#qbi-zz1z0ieo div.card-menu-wr #qbi-zz1z0ieo svg.svg-icon → 0 匹配 ❌
          // 正确拼法：#qbi-zz1z0ieo div.card-menu-wr svg.svg-icon → 1 匹配 ✅
          let localSelector = selector;
          if (selector.startsWith(recentHover.stableId + ' ')) {
            localSelector = selector.substring(recentHover.stableId.length + 1);
          } else if (selector.startsWith(recentHover.stableId)) {
            localSelector = selector.substring(recentHover.stableId.length).trim();
          }
          
          if (recentHover.selector && localSelector) {
            // 尝试1：hover 完整选择器 + 去重后的 click 选择器
            const enhancedSelectorFull = `${recentHover.selector} ${localSelector}`;
            // 验证：拼接后必须实际存在（querySelectorAll 不支持 :has-text，跳过含伪类的）
            if (!localSelector.includes(':has-text') && !localSelector.includes(':text')) {
              try {
                const matchesFull = document.querySelectorAll(enhancedSelectorFull);
                if (matchesFull.length === 1) {
                  selector = enhancedSelectorFull;
                  grade = 'A';
                  matchCount = 1;
                  strategy = 'hover-context';
                }
              } catch {}
            }
          }
          // 尝试2（降级）：用祖先 ID + 去重后的 click 选择器
          if (matchCount !== 1 && localSelector) {
            const enhancedSelectorId = `${recentHover.stableId} ${localSelector}`;
            if (!localSelector.includes(':has-text') && !localSelector.includes(':text')) {
              try {
                const matchesId = document.querySelectorAll(enhancedSelectorId);
                if (matchesId.length === 1) {
                  selector = enhancedSelectorId;
                  grade = 'A';
                  matchCount = 1;
                  strategy = 'hover-context';
                }
              } catch {}
            }
          }
          // 尝试3（最终降级）：用原始 click selector（含 :has-text 等伪类时 querySelectorAll 不支持）
          // 此时保持原 selector 不变，不强行拼接
        }
      }
      
      // New: Enhance selector with click-trigger context (for dropdown/popover)
      // If click is in a floating layer (ant-dropdown, popover, modal) and selector is low-quality,
      // use the most recent click's stable ID as parent qualifier
      const recentClickTrigger = (window as any).__rpa_lastClickTrigger;
      if ((grade === 'C' || grade === 'D') && recentClickTrigger && recentClickTrigger.stableId) {
        // Check if target is in a floating layer (dropdown, popover, modal)
        const isFloatingLayer = target.closest('.ant-dropdown, .ant-popover, .ant-modal, [class*="dropdown"], [class*="popover"], [class*="popup"]');
        
        if (isFloatingLayer) {
          // Check if the floating layer appeared after the trigger click (within 3 seconds)
          if (now - recentClickTrigger.timestamp < 3000) {
            // Use trigger's stable ID as context
            const enhancedSelector = `${recentClickTrigger.stableId} ${selector}`;
            const enhancedMatches = document.querySelectorAll(enhancedSelector);
            if (enhancedMatches.length === 1) {
              selector = enhancedSelector;
              grade = 'A';
              matchCount = 1;
              strategy = 'click-trigger';
            }
          }
        }
      }
      
      // Record this click as potential trigger for future dropdown/popover interactions
      // Only record if this click has a stable ID (S/A/B grade)
      if (grade === 'S' || grade === 'A' || grade === 'B') {
        // Find the closest element with stable ID
        let triggerEl: HTMLElement | null = target;
        let triggerStableId = '';
        for (let i = 0; i < 10 && triggerEl; i++) {
          if (triggerEl.id && isStableIdentifier(triggerEl.id)) {
            triggerStableId = `#${triggerEl.id}`;
            break;
          }
          triggerEl = triggerEl.parentElement;
        }
        
        if (triggerStableId) {
          (window as any).__rpa_lastClickTrigger = {
            stableId: triggerStableId,
            timestamp: now,
            url: location.href
          };
        }
      }
      
      const actionIndex = (window as any).__rpa_actions.length;
      (window as any).__rpa_actions.push({
        type: 'click', timestamp: now, url: location.href,
        target: selector, targetText: target.textContent?.trim().substring(0, 80), targetTag: target.tagName?.toLowerCase(),
        // Validation fields
        stabilityGrade: grade, uniquenessMatch: matchCount, selectorStrategy: strategy,
        // New: record if this click was enhanced by trigger context
        triggeredByClick: strategy === 'click-trigger' ? recentClickTrigger?.stableId : undefined,
        // v8.1.0: 候选选择器列表
        candidates: candidates,
        confidence: quick.found ? 0.95 : (matchCount === 1 ? 0.8 : 0.5),
      });

      // v8.1.0: 推入异步队列补充更完整的候选列表
      if (!quick.found) {
        scheduleSelectorAnalysis(actionIndex, snapshot);
      }
    }, { capture: true, passive: true });

    document.addEventListener('change', (e: Event) => {
      if (!e.isTrusted) return;
      const target = e.target as HTMLInputElement;
      if (!target || !['INPUT', 'SELECT', 'TEXTAREA'].includes(target.tagName)) return;

      // v8.1.0: 混合策略
      const snapshot = captureSnapshot(target);
      const quick = quickValidation(target, snapshot);
      let selector: string, grade: string, matchCount: number, strategy: string;
      if (quick.found) {
        selector = quick.selector!; grade = quick.grade!; matchCount = quick.matchCount!; strategy = quick.strategy!;
      } else {
        const result = buildUniqueSelector(target);
        selector = result.selector; grade = result.grade; matchCount = result.matchCount; strategy = result.strategy;
      }

      // ── File upload detection (input[type=file]) ──
      if (target.tagName === 'INPUT' && target.type === 'file') {
        const files = target.files;
        const fileInfo = files && files.length > 0 ? files[0] : null;
        const actionIndex = (window as any).__rpa_actions.length;
        (window as any).__rpa_actions.push({
          type: 'upload', timestamp: Date.now(), url: location.href,
          target: selector, targetText: target.getAttribute('accept') || 'file input',
          targetType: 'file',
          fileName: fileInfo?.name || (files && files.length > 1 ? `${files.length} files` : ''),
          fileSize: fileInfo?.size || 0,
          value: fileInfo?.name || '[file]',
          stabilityGrade: grade, uniquenessMatch: matchCount, selectorStrategy: strategy,
          candidates: quick.candidates, confidence: quick.found ? 0.95 : (matchCount === 1 ? 0.8 : 0.5),
        });
        if (!quick.found) scheduleSelectorAnalysis(actionIndex, snapshot);
        return;
      }

      const sensitive = isSensitiveField(target);
      const value = target.type === 'password' ? '[REDACTED]' : (sensitive ? '[SENSITIVE-REDACTED]' : (target.value || '').substring(0, 500));
      const actionIndex = (window as any).__rpa_actions.length;
      (window as any).__rpa_actions.push({
        type: target.tagName === 'SELECT' ? 'select' : 'input', timestamp: Date.now(), url: location.href,
        target: selector, targetType: target.type || target.tagName.toLowerCase(), name: target.name, value,
        stabilityGrade: grade, uniquenessMatch: matchCount, selectorStrategy: strategy, sensitiveField: sensitive,
        candidates: quick.candidates, confidence: quick.found ? 0.95 : (matchCount === 1 ? 0.8 : 0.5),
      });
      if (!quick.found) scheduleSelectorAnalysis(actionIndex, snapshot);
    }, { capture: true, passive: true });

    document.addEventListener('submit', (e: SubmitEvent) => {
      if (!e.isTrusted) return;
      const form = e.target as HTMLFormElement;
      if (!form) return;

      // v8.1.0: 混合策略
      const snapshot = captureSnapshot(form);
      const quick = quickValidation(form, snapshot);
      let selector: string, grade: string, matchCount: number, strategy: string;
      if (quick.found) {
        selector = quick.selector!; grade = quick.grade!; matchCount = quick.matchCount!; strategy = quick.strategy!;
      } else {
        const result = buildUniqueSelector(form);
        selector = result.selector; grade = result.grade; matchCount = result.matchCount; strategy = result.strategy;
      }

      const fields: Record<string, string> = {};
      const fd = new FormData(form);
      fd.forEach((v, k) => {
        const keyLower = k.toLowerCase();
        if (keyLower.includes('password') || keyLower.includes('passwd')) {
          fields[k] = '[REDACTED]';
        } else if (/id_?card|bank_?card|phone|mobile|ssn|cvv/.test(keyLower)) {
          fields[k] = '[SENSITIVE-REDACTED]';
        } else {
          fields[k] = typeof v === 'string' ? v.substring(0, 200) : '[file]';
        }
      });
      const actionIndex = (window as any).__rpa_actions.length;
      (window as any).__rpa_actions.push({
        type: 'submit', timestamp: Date.now(), url: location.href, target: selector, fields,
        stabilityGrade: grade, uniquenessMatch: matchCount, selectorStrategy: strategy,
        candidates: quick.candidates, confidence: quick.found ? 0.95 : (matchCount === 1 ? 0.8 : 0.5),
      });
      if (!quick.found) scheduleSelectorAnalysis(actionIndex, snapshot);
    }, { capture: true, passive: true });

    // ── Keyboard event listener (keydown) ──
    // Captures meaningful keys: Enter, Tab, Escape, arrows, shortcuts (Ctrl+C, etc.)
    // Filters out: standalone modifier keys, repeat holds
    const MODIFIER_KEYS = new Set(['Control', 'Shift', 'Alt', 'Meta']);
    const MEANINGFUL_KEYS = new Set([
      'Enter', 'Tab', 'Escape', 'Backspace', 'Delete',
      'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight',
      'Home', 'End', 'PageUp', 'PageDown',
    ]);

    document.addEventListener('keydown', (e: KeyboardEvent) => {
      if (!e.isTrusted) return;
      if (e.repeat) return;  // Skip key repeat (holding down)
      if (MODIFIER_KEYS.has(e.key) && !e.ctrlKey && !e.shiftKey && !e.altKey && !e.metaKey) return;  // Skip standalone modifier press

      const target = e.composedPath()[0] as HTMLElement;
      if (!target) return;

      // Only capture if target is an interactive element or if it's a shortcut
      const isInteractive = ['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName) || target.isContentEditable;
      const hasModifier = e.ctrlKey || e.shiftKey || e.altKey || e.metaKey;
      const isMeaningful = MEANINGFUL_KEYS.has(e.key) || e.key === 'Tab';

      if (!isInteractive && !hasModifier && !isMeaningful) return;

      // v8.1.0: 混合策略
      const snapshot = captureSnapshot(target);
      const quick = quickValidation(target, snapshot);
      let selector: string, grade: string, matchCount: number, strategy: string;
      if (quick.found) {
        selector = quick.selector!; grade = quick.grade!; matchCount = quick.matchCount!; strategy = quick.strategy!;
      } else {
        const result = buildUniqueSelector(target);
        selector = result.selector; grade = result.grade; matchCount = result.matchCount; strategy = result.strategy;
      }

      const modifiers: string[] = [];
      if (e.ctrlKey) modifiers.push('Ctrl');
      if (e.shiftKey) modifiers.push('Shift');
      if (e.altKey) modifiers.push('Alt');
      if (e.metaKey) modifiers.push('Meta');

      const actionIndex = (window as any).__rpa_actions.length;
      (window as any).__rpa_actions.push({
        type: 'keydown', timestamp: Date.now(), url: location.href,
        target: selector, targetText: target.textContent?.trim().substring(0, 40),
        targetType: target.tagName?.toLowerCase(),
        key: e.key, keyModifiers: modifiers.length > 0 ? modifiers : undefined,
        value: modifiers.length > 0 ? `${modifiers.join('+')}+${e.key}` : e.key,
        stabilityGrade: grade, uniquenessMatch: matchCount, selectorStrategy: strategy,
        candidates: quick.candidates, confidence: quick.found ? 0.95 : (matchCount === 1 ? 0.8 : 0.5),
      });
      if (!quick.found) scheduleSelectorAnalysis(actionIndex, snapshot);
    }, { capture: true, passive: true });

    // ── Drag & Drop event listener ──
    // Captures HTML5 native drag-and-drop (drop event)
    document.addEventListener('drop', (e: DragEvent) => {
      if (!e.isTrusted) return;
      const target = e.composedPath()[0] as HTMLElement;
      if (!target) return;

      const { selector, grade, matchCount, strategy } = buildUniqueSelector(target);

      // Try to get drag data (files or text)
      let dragInfo: any = {};
      if (e.dataTransfer) {
        if (e.dataTransfer.files.length > 0) {
          dragInfo.fileName = e.dataTransfer.files[0].name;
          dragInfo.fileSize = e.dataTransfer.files[0].size;
          dragInfo.fileCount = e.dataTransfer.files.length;
        }
        try {
          const textData = e.dataTransfer.getData('text/plain');
          if (textData) dragInfo.dragText = textData.substring(0, 200);
        } catch {}
        try {
          const uriData = e.dataTransfer.getData('text/uri-list');
          if (uriData) dragInfo.dragUri = uriData.split('\n')[0].trim();
        } catch {}
      }

      (window as any).__rpa_actions.push({
        type: 'drag', timestamp: Date.now(), url: location.href,
        target: selector, targetText: target.textContent?.trim().substring(0, 80),
        targetType: target.tagName?.toLowerCase(),
        value: dragInfo.fileName || dragInfo.dragText || 'drop',
        fileName: dragInfo.fileName,
        fileSize: dragInfo.fileSize,
        stabilityGrade: grade, uniquenessMatch: matchCount, selectorStrategy: strategy,
      });
    }, { capture: true, passive: true });

    // ── Scroll event listener ──
    // Captures scroll actions with throttling (500ms) to avoid flooding
    // Critical for: lazy loading, infinite scroll, virtual lists
    let __rpa_lastScrollTime = 0;
    let __rpa_lastScrollTop = 0;
    const SCROLL_THROTTLE_MS = 500;

    function handleScroll(e: Event) {
      const now = Date.now();
      if (now - __rpa_lastScrollTime < SCROLL_THROTTLE_MS) return;
      __rpa_lastScrollTime = now;

      const isWindow = e.target === document || e.target === document.documentElement;
      const scrollTop = isWindow ? window.scrollY || document.documentElement.scrollTop : (e.target as HTMLElement).scrollTop;
      const direction: 'up' | 'down' = scrollTop > __rpa_lastScrollTop ? 'down' : 'up';
      __rpa_lastScrollTop = scrollTop;

      const target = isWindow ? document.documentElement : (e.target as HTMLElement);
      const { selector, grade } = buildUniqueSelector(target);

      (window as any).__rpa_actions.push({
        type: 'scroll', timestamp: now, url: location.href,
        target: selector,
        targetText: isWindow ? 'window' : (target.textContent?.trim().substring(0, 40) || target.className?.substring(0, 40)),
        targetType: isWindow ? 'window' : target.tagName?.toLowerCase(),
        scrollTarget: isWindow ? 'window' : (target.className?.substring(0, 60) || target.id || target.tagName),
        scrollTop: scrollTop,
        scrollDirection: direction,
        value: `${direction} ${Math.round(scrollTop)}px`,
        stabilityGrade: grade, uniquenessMatch: 1, selectorStrategy: 'scroll',
      });
    }

    // Capture scroll on window and all scrollable containers
    window.addEventListener('scroll', handleScroll, { capture: true, passive: true });
    // Also listen on document for non-window scroll containers
    document.addEventListener('scroll', handleScroll, { capture: true, passive: true });

    // ── Mouseenter/Hover event listener ──
    // Captures hover events that reveal hidden elements (menus, tooltips, floating buttons)
    // Only records if the element has interactive children or is itself interactive
    // Throttled to avoid flooding (1000ms per unique element)
    const __rpa_hoverCache = new Map<string, number>();
    const __rpa_hoverStartTime = new Map<string, number>();  // Track hover start for duration
    // Fix #3: Track last significant hover (with stable ID) for click context correlation
    (window as any).__rpa_lastSignificantHover = { selector: '', timestamp: 0, stableId: '' };
    const HOVER_THROTTLE_MS = 1000;

    document.addEventListener('mouseenter', (e: MouseEvent) => {
      const target = e.composedPath()[0] as HTMLElement;
      if (!target || target.nodeType !== 1) return;

      const now = Date.now();

      // v8.1.0: 混合策略
      const snapshot = captureSnapshot(target);
      const quick = quickValidation(target, snapshot);
      let baseSelector: string, grade: string, matchCount: number, strategy: string;
      if (quick.found) {
        baseSelector = quick.selector!; grade = quick.grade!; matchCount = quick.matchCount!; strategy = quick.strategy!;
      } else {
        const result = buildUniqueSelector(target);
        baseSelector = result.selector; grade = result.grade; matchCount = result.matchCount; strategy = result.strategy;
      }

      // Throttle: skip if same element hovered recently
      const lastHover = __rpa_hoverCache.get(baseSelector);
      if (lastHover && now - lastHover < HOVER_THROTTLE_MS) return;
      __rpa_hoverCache.set(baseSelector, now);
      
      // Track hover start time for duration calculation
      __rpa_hoverStartTime.set(baseSelector, now);
      
      // Fix #3: Track significant hover (element with stable ID or long hover duration)
      // This helps correlate hover context with subsequent click events
      if (strategy === 'stable-id' || strategy.startsWith('parent-')) {
        // Find the closest ancestor with a stable ID for context
        let hoverStableId = '';
        let ancestor: HTMLElement | null = target;
        for (let i = 0; i < 10 && ancestor; i++) {
          if (ancestor.id && isStableIdentifier(ancestor.id)) {
            hoverStableId = `#${ancestor.id}`;
            break;
          }
          ancestor = ancestor.parentElement;
        }
        if (hoverStableId) {
          (window as any).__rpa_lastSignificantHover = {
            selector: baseSelector,
            timestamp: now,
            stableId: hoverStableId
          };
        }
      }

      // Only record hover on elements that are likely to reveal something:
      const isInteractive = target.hasAttribute('title') ||
        target.getAttribute('role')?.includes('menu') ||
        target.closest('[class*="dropdown"]') !== null ||
        target.closest('[class*="popover"]') !== null ||
        target.closest('[class*="tooltip"]') !== null ||
        target.tagName === 'TR' ||
        target.querySelector('[class*="action"]') !== null ||
        target.querySelector('[class*="menu"]') !== null ||
        target.querySelector('[class*="hidden"]') !== null ||
        target.querySelector('[style*="display: none"]') !== null;

      if (!isInteractive) return;

      const actionIndex = (window as any).__rpa_actions.length;
      (window as any).__rpa_actions.push({
        type: 'mouseenter', timestamp: now, url: location.href,
        target: baseSelector,
        targetText: target.textContent?.trim().substring(0, 60),
        targetType: target.tagName?.toLowerCase(),
        hoverTarget: baseSelector,
        value: target.textContent?.trim().substring(0, 40) || target.className?.substring(0, 40),
        stabilityGrade: grade, uniquenessMatch: matchCount, selectorStrategy: strategy,
        candidates: quick.candidates, confidence: quick.found ? 0.95 : (matchCount === 1 ? 0.8 : 0.5),
      });
      if (!quick.found) scheduleSelectorAnalysis(actionIndex, snapshot);
    }, { capture: true, passive: true });
    
    // Track hover duration: record when mouse leaves an element
    document.addEventListener('mouseleave', (e: MouseEvent) => {
      const target = e.composedPath()[0] as HTMLElement;
      if (!target || target.nodeType !== 1) return;
      
      const now = Date.now();
      const { selector } = buildUniqueSelector(target);
      const startTime = __rpa_hoverStartTime.get(selector);
      if (startTime) {
        const duration = now - startTime;
        // Update the last mouseenter action with hover duration (Fix #11)
        const actions = (window as any).__rpa_actions;
        for (let i = actions.length - 1; i >= 0; i--) {
          if (actions[i].type === 'mouseenter' && actions[i].target === selector) {
            actions[i].hoverDuration = duration;
            break;
          }
        }
        __rpa_hoverStartTime.delete(selector);
      }
    }, { capture: true, passive: true });

    // ── Dblclick event listener ──
    document.addEventListener('dblclick', (e: MouseEvent) => {
      if (!e.isTrusted) return;
      const target = e.composedPath()[0] as HTMLElement;
      if (!target) return;
      const { selector, grade, matchCount, strategy } = buildUniqueSelector(target);

      (window as any).__rpa_actions.push({
        type: 'dblclick', timestamp: Date.now(), url: location.href,
        target: selector,
        targetText: target.textContent?.trim().substring(0, 80),
        targetType: target.tagName?.toLowerCase(),
        value: 'dblclick',
        stabilityGrade: grade, uniquenessMatch: matchCount, selectorStrategy: strategy,
      });
    }, { capture: true, passive: true });

    // ── Wheel event listener ──
    let __rpa_lastWheelTime = 0;
    const WHEEL_THROTTLE_MS = 1000;

    document.addEventListener('wheel', (e: WheelEvent) => {
      if (!e.isTrusted) return;
      const now = Date.now();
      if (now - __rpa_lastWheelTime < WHEEL_THROTTLE_MS) return;
      __rpa_lastWheelTime = now;

      const target = e.composedPath()[0] as HTMLElement;
      if (!target || (target as any) === document || target === document.documentElement) return;

      const isSpecialContainer = target.tagName === 'CANVAS' ||
        target.closest('[class*="chart"]') !== null ||
        target.closest('[class*="map"]') !== null ||
        target.closest('[class*="zoom"]') !== null ||
        target.closest('[style*="overflow"]') !== null ||
        target.getAttribute('role') === 'application';

      if (!isSpecialContainer) return;

      const { selector, grade, matchCount, strategy } = buildUniqueSelector(target);

      (window as any).__rpa_actions.push({
        type: 'wheel', timestamp: now, url: location.href,
        target: selector,
        targetText: target.textContent?.trim().substring(0, 40),
        targetType: target.tagName?.toLowerCase(),
        wheelDeltaX: e.deltaX,
        wheelDeltaY: e.deltaY,
        value: `wheel(${Math.round(e.deltaX)}, ${Math.round(e.deltaY)})`,
        stabilityGrade: grade, uniquenessMatch: matchCount, selectorStrategy: strategy,
      });
    }, { capture: true, passive: true });

    // ── Focus event listener ──
    // Defer buildUniqueSelector to next frame to avoid blocking render (prevents flash)
    document.addEventListener('focusin', (e: FocusEvent) => {
      const target = e.target as HTMLElement;
      if (!target || !['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName)) return;
      if (target.isContentEditable) return;

      const ts = Date.now();
      const targetText = target.getAttribute('placeholder') || target.getAttribute('name') || target.textContent?.trim().substring(0, 40);
      const targetType = (target as HTMLInputElement).type || target.tagName.toLowerCase();

      // v8.1.0: 同步采集快照（元素还在DOM中）
      const snapshot = captureSnapshot(target);

      requestAnimationFrame(() => {
        // v8.1.0: 混合策略
        const quick = quickValidation(target, snapshot);
        let selector: string, grade: string, matchCount: number, strategy: string;
        if (quick.found) {
          selector = quick.selector!; grade = quick.grade!; matchCount = quick.matchCount!; strategy = quick.strategy!;
        } else if (document.contains(target)) {
          const result = buildUniqueSelector(target);
          selector = result.selector; grade = result.grade; matchCount = result.matchCount; strategy = result.strategy;
        } else {
          // 元素已移除，用快照生成降级选择器
          const candidates = analyzeFromSnapshot(snapshot);
          const best = candidates[0];
          selector = best?.selector || snapshot.tag;
          grade = best?.grade || 'C';
          matchCount = best?.matchCount || -1;
          strategy = best?.strategy || 'snapshot-fallback';
        }
        const actionIndex = (window as any).__rpa_actions.length;
        (window as any).__rpa_actions.push({
          type: 'focus', timestamp: ts, url: location.href,
          target: selector, targetText, targetType,
          focusDirection: 'in',
          value: 'focus',
          stabilityGrade: grade, uniquenessMatch: matchCount, selectorStrategy: strategy,
          candidates: quick?.candidates, confidence: quick?.found ? 0.95 : (matchCount === 1 ? 0.8 : 0.5),
        });
        if (!quick?.found && matchCount !== 1) scheduleSelectorAnalysis(actionIndex, snapshot);
      });
    }, { capture: true, passive: true });

    // ── Blur event listener ──
    // Defer buildUniqueSelector to next frame to avoid blocking render (prevents flash)
    document.addEventListener('focusout', (e: FocusEvent) => {
      const target = e.target as HTMLElement;
      if (!target || !['INPUT', 'TEXTAREA', 'SELECT'].includes(target.tagName)) return;

      const ts = Date.now();
      const targetText = target.getAttribute('placeholder') || target.getAttribute('name') || target.textContent?.trim().substring(0, 40);
      const targetType = (target as HTMLInputElement).type || target.tagName.toLowerCase();

      // v8.1.0: 同步采集快照（元素还在DOM中）
      const snapshot = captureSnapshot(target);

      requestAnimationFrame(() => {
        // v8.1.0: 混合策略
        const quick = quickValidation(target, snapshot);
        let selector: string, grade: string, matchCount: number, strategy: string;
        if (quick.found) {
          selector = quick.selector!; grade = quick.grade!; matchCount = quick.matchCount!; strategy = quick.strategy!;
        } else if (document.contains(target)) {
          const result = buildUniqueSelector(target);
          selector = result.selector; grade = result.grade; matchCount = result.matchCount; strategy = result.strategy;
        } else {
          // 元素已移除，用快照生成降级选择器
          const candidates = analyzeFromSnapshot(snapshot);
          const best = candidates[0];
          selector = best?.selector || snapshot.tag;
          grade = best?.grade || 'C';
          matchCount = best?.matchCount || -1;
          strategy = best?.strategy || 'snapshot-fallback';
        }
        const actionIndex = (window as any).__rpa_actions.length;
        (window as any).__rpa_actions.push({
          type: 'blur', timestamp: ts, url: location.href,
          target: selector, targetText, targetType,
          focusDirection: 'out',
          value: 'blur',
          stabilityGrade: grade, uniquenessMatch: matchCount, selectorStrategy: strategy,
          candidates: quick?.candidates, confidence: quick?.found ? 0.95 : (matchCount === 1 ? 0.8 : 0.5),
        });
        if (!quick?.found && matchCount !== 1) scheduleSelectorAnalysis(actionIndex, snapshot);
      });
    }, { capture: true, passive: true });

    // ── Resize event listener ──
    let __rpa_lastResizeTime = 0;
    const RESIZE_THROTTLE_MS = 2000;

    window.addEventListener('resize', () => {
      const now = Date.now();
      if (now - __rpa_lastResizeTime < RESIZE_THROTTLE_MS) return;
      __rpa_lastResizeTime = now;

      (window as any).__rpa_actions.push({
        type: 'resize', timestamp: now, url: location.href,
        target: 'window',
        targetText: 'viewport resize',
        targetType: 'window',
        viewportWidth: window.innerWidth,
        viewportHeight: window.innerHeight,
        value: `${window.innerWidth}x${window.innerHeight}`,
        stabilityGrade: 'S', uniquenessMatch: 1, selectorStrategy: 'resize',
      });
    }, { passive: true });

    // ── Contextmenu event listener ──
    document.addEventListener('contextmenu', (e: MouseEvent) => {
      if (!e.isTrusted) return;
      const target = e.composedPath()[0] as HTMLElement;
      if (!target) return;

      const { selector, grade, matchCount, strategy } = buildUniqueSelector(target);

      (window as any).__rpa_actions.push({
        type: 'contextmenu', timestamp: Date.now(), url: location.href,
        target: selector,
        targetText: target.textContent?.trim().substring(0, 80),
        targetType: target.tagName?.toLowerCase(),
        contextMenuTarget: selector,
        value: 'right-click',
        stabilityGrade: grade, uniquenessMatch: matchCount, selectorStrategy: strategy,
      });
    }, { capture: true, passive: true });

    // ── Download DOM changes observer (v6.5) ──
    // 检测 iframe 创建（某些系统用隐藏 iframe 触发下载）
    // 检测 Blob URL 锚点创建（前端生成文件后动态创建 <a href="blob:...">）
    (window as any).__rpa_downloadDomChanges = {
      iframeCreated: false,
      iframeSrcs: [] as string[],
      blobUrlAnchors: false,
      hiddenFormSubmit: false,
    };
    
    const downloadObserver = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        for (const node of Array.from(mutation.addedNodes)) {
          if (!(node instanceof Element)) continue;
          
          // 检测 iframe 创建
          if (node.tagName === 'IFRAME') {
            const iframe = node as HTMLIFrameElement;
            (window as any).__rpa_downloadDomChanges.iframeCreated = true;
            if (iframe.src) {
              (window as any).__rpa_downloadDomChanges.iframeSrcs.push(iframe.src);
            }
          }
          
          // 检测 Blob URL 锚点
          if (node.tagName === 'A') {
            const anchor = node as HTMLAnchorElement;
            if (anchor.href && anchor.href.startsWith('blob:')) {
              (window as any).__rpa_downloadDomChanges.blobUrlAnchors = true;
            }
          }
          
          // 检测子元素中的 iframe 和 blob anchor
          const iframes = node.querySelectorAll?.('iframe') || [];
          iframes.forEach((iframe: Element) => {
            (window as any).__rpa_downloadDomChanges.iframeCreated = true;
            if ((iframe as HTMLIFrameElement).src) {
              (window as any).__rpa_downloadDomChanges.iframeSrcs.push((iframe as HTMLIFrameElement).src);
            }
          });
          
          const blobAnchors = node.querySelectorAll?.('a[href^="blob:"]') || [];
          if (blobAnchors.length > 0) {
            (window as any).__rpa_downloadDomChanges.blobUrlAnchors = true;
          }
        }
      }
    });
    
    downloadObserver.observe(document.body || document.documentElement, {
      childList: true,
      subtree: true,
    });
  });

  // ── Network capture (context level — all tabs) ─────────────────────────────
  context.on('request', (req: Request) => {
    if (!shouldCapture(req)) return;
    const id = `req_${String(++seqCounter).padStart(4, '0')}`;
    requestIndex.set(req, id);
    const { raw, parsed } = extractPostData(req);
    requests.push({ id, seqNum: seqCounter, timestamp: Date.now(), relativeMs: Date.now() - startTime, method: req.method(), url: req.url(), headers: req.headers(), postData: raw, postDataParsed: parsed, resourceType: req.resourceType() });
  });

  context.on('response', async (res: Response) => {
    const id = requestIndex.get(res.request());
    if (!id) return;
    const contentType = res.headers()['content-type'] || '';
    const isText = /json|text|xml|form|javascript|graphql/.test(contentType);
    let body: string | null = null;
    let bodyParsed: any;
    let truncated = false;
    let bodySummary: { topLevelKeys: string[]; keyFields: Record<string, any> } | undefined;
    let bodySaved = false;
    let bodySaveReason: string | undefined;
    
    if (isText) {
      try {
        const raw = await res.text();
        if (raw.length > MAX_BODY_SIZE) { body = raw.substring(0, MAX_BODY_SIZE); truncated = true; } else { body = raw; }
        bodyParsed = tryParseJSON(body);
      } catch {}
    }
    
    // v6.5: 下载特征标注（不影响现有逻辑，只增加元数据）
    const isFile = isFileDownloadResponse(res.headers(), contentType);
    let hasTaskId = false;
    let taskIdPath: string | undefined;
    if (bodyParsed) {
      taskIdPath = findTaskIdField(bodyParsed) || undefined;
      hasTaskId = !!taskIdPath;
    }
    
    // v6.6: 根据白名单决定是否保存完整 body
    const saveFull = opts.saveFull;
    const url = res.request().url();
    const shouldSaveBody = saveFull || 
                           isWhitelistedUrl(url) || 
                           isFile || 
                           hasTaskId;
    
    if (shouldSaveBody) {
      bodySaved = true;
      if (isWhitelistedUrl(url)) bodySaveReason = 'whiteList';
      else if (isFile) bodySaveReason = 'fileResponse';
      else if (hasTaskId) bodySaveReason = 'taskId';
      else bodySaveReason = 'saveFull';
    } else {
      // 不保存完整 body，只保存摘要
      body = null;
      if (bodyParsed) {
        bodySummary = extractBodySummary(bodyParsed);
      }
      bodySaved = false;
    }
    
    // v8.3.0: 大数组截断（减少 recording.json 体积）
    // 触发条件：响应体 > 60KB 且包含 > 20 行的数组
    let arrayTruncatedInfo: Array<{ path: string; originalCount: number; keptCount: number }> | undefined;
    const originalBodyForBackup = body;  // 保存原始 body 用于 bodiesStream 备份
    if (body && shouldSaveBody) {
      const truncateResult = truncateLargeArrays(body);
      if (truncateResult.truncated) {
        body = truncateResult.body;
        arrayTruncatedInfo = truncateResult.truncatedArrays;
        // 输出截断信息（方便调试）
        for (const arr of arrayTruncatedInfo) {
          console.log(`  📐 截断大数组: ${arr.path} (${arr.originalCount} → ${arr.keptCount} 元素)`);
        }
      }
    }
    
    // v8.3.0: JSON字符串摘要（减少 recording.json 体积）
    // 触发条件：响应体 > 60KB 且字符串 > 5KB 且能解析为JSON
    let stringSummarizedInfo: Array<{ path: string; originalSize: number; keyCount: number }> | undefined;
    if (body && shouldSaveBody) {
      const summarizeResult = summarizeJsonStrings(body);
      if (summarizeResult.summarized) {
        body = summarizeResult.body;
        stringSummarizedInfo = summarizeResult.summarizedStrings;
        // 输出摘要信息（方便调试）
        for (const s of stringSummarizedInfo) {
          console.log(`  📝 JSON摘要: ${s.path} (${(s.originalSize/1024).toFixed(1)}KB, ${s.keyCount}字段)`);
        }
      }
    }
    
    responses[id] = { 
      requestId: id, timestamp: Date.now(), status: res.status(), statusText: res.statusText(), 
      headers: res.headers(), mimeType: contentType, body, truncated, 
      isRedirect: res.status() >= 300 && res.status() < 400,
      // v6.5 新增字段
      isFileResponse: isFile || undefined,
      containsTaskId: hasTaskId || undefined,
      taskIdField: taskIdPath,
      // v6.6 新增字段
      bodySummary,
      bodySaved,
      bodySaveReason,
      // v8.3.0 新增字段
      arrayTruncated: arrayTruncatedInfo,
      stringSummarized: stringSummarizedInfo,
    };

    // v7.4.1: 所有响应体都写入 bodies 文件（作为备份，测试阶段可查）
    // v8.3.0: 使用原始完整 body（截断前）
    if (originalBodyForBackup && isText) {
      const bodyRecord = {
        requestId: id,
        timestamp: Date.now(),
        url: res.request().url(),
        status: res.status(),
        bodySaved,
        body: originalBodyForBackup  // 使用原始完整 body
      };
      bodiesStream.write(JSON.stringify(bodyRecord) + '\n');
    }
  });

  // ── Create page AFTER init script is injected (v6.7 fix) ───────────────────
  // 这样确保页面第一次加载时就有监听器，包括重定向场景
  const page: Page = await context.newPage();

  // ── v7.5.0: 下载文件实时保存 + 表头提取（提前定义，供所有页面使用）────────
  const downloadedFilesDir = path.join(outputDir, 'downloaded-files');
  let downloadFileIndex = 0;

  async function saveDownloadAndExtractHeaders(download: any): Promise<Partial<DownloadEvent>> {
    const result: Partial<DownloadEvent> = {};
    try {
      if (!fs.existsSync(downloadedFilesDir)) {
        fs.mkdirSync(downloadedFilesDir, { recursive: true });
      }

      downloadFileIndex++;
      const originalName = download.suggestedFilename() || `download_${downloadFileIndex}`;
      const safeName = `${String(downloadFileIndex).padStart(2, '0')}_${originalName.replace(/[<>:"|?*]/g, '_')}`;
      const savePath = path.join(downloadedFilesDir, safeName);

      await download.saveAs(savePath);
      result.savedPath = savePath;

      const stat = fs.statSync(savePath);
      result.fileSize = stat.size;
      process.stdout.write(`  💾 [download] Saved: ${safeName} (${(stat.size / 1024).toFixed(1)} KB)\n`);

      // 提取表头
      const ext = path.extname(originalName).toLowerCase();
      if (['.xlsx', '.xls', '.xlsm'].includes(ext)) {
        try {
          const ExcelJS = require('exceljs');
          const workbook = new ExcelJS.Workbook();
          await workbook.xlsx.readFile(savePath);
          const worksheet = workbook.worksheets[0];
          if (worksheet && worksheet.rowCount > 0) {
            const headerRow = worksheet.getRow(1);
            const headers: string[] = [];
            headerRow.eachCell((cell: any, colNumber: number) => {
              headers.push(cell.value?.toString() || `Column${colNumber}`);
            });
            result.headers = headers;
            process.stdout.write(`  📊 [download] Headers: ${headers.join(', ')}\n`);
          }
        } catch (err: any) {
          process.stdout.write(`  ⚠️ [download] Failed to read ${ext}: ${err.message}\n`);
        }
      } else if (['.csv', '.tsv'].includes(ext)) {
        try {
          const content = fs.readFileSync(savePath, 'utf-8');
          const firstLine = content.split('\n')[0];
          const separator = ext === '.tsv' ? '\t' : ',';
          result.headers = firstLine.split(separator).map((h: string) => h.trim().replace(/^"|"$/g, ''));
          process.stdout.write(`  📊 [download] Headers: ${result.headers.join(', ')}\n`);
        } catch (err: any) {
          process.stdout.write(`  ⚠️ [download] Failed to read ${ext}: ${err.message}\n`);
        }
      }

      // 关联 API 请求：找到下载前 3 秒内的 POST 请求
      // 注意：此时还没检测轮询模式，所以先记录所有 POST，后面再过滤
      const downloadTime = Date.now();
      const relatedReqs = requests.filter(r => {
        if (r.method !== 'POST') return false;
        if (r.timestamp > downloadTime || r.timestamp < downloadTime - 3000) return false;
        return true;
      });
      result.relatedRequestIds = relatedReqs.map(r => r.id);
      if (relatedReqs.length > 0) {
        process.stdout.write(`  🔗 [download] Related APIs: ${relatedReqs.length} POST request(s) in last 3s\n`);
      }
    } catch (err: any) {
      process.stdout.write(`  ⚠️ [download] Save failed: ${err.message}\n`);
    }
    return result;
  }

  // ── Navigation tracking (all tabs) ────────────────────────────────────────
  context.on('page', (newPage) => {
    process.stdout.write(`  🆕 New tab: ${newPage.url() || '(loading)'}\n`);
    newPage.on('framenavigated', (frame) => {
      if (frame !== newPage.mainFrame()) return;
      const url = frame.url();
      actions.push({ seqNum: ++seqCounter, timestamp: Date.now(), relativeMs: Date.now() - startTime, type: 'navigate', url, label: `[new-tab] ${url}` });
      process.stdout.write(`  ↗  [tab] ${url.substring(0, 100)}\n`);
    });
    // v7.5.0: 监听新页面的下载事件（实时保存 + 表头提取）
    newPage.on('download', async (download) => {
      try {
        const savedInfo = await saveDownloadAndExtractHeaders(download);
        downloadEvents.push({
          timestamp: Date.now(),
          relativeMs: Date.now() - startTime,
          url: download.url(),
          suggestedFilename: download.suggestedFilename(),
          mimeType: '',
          ...savedInfo,
        });
        process.stdout.write(`  📥 [new-tab] Download: ${download.suggestedFilename()}\n`);
      } catch (err) {
        process.stdout.write(`  ⚠️ [new-tab] Download event error: ${err}\n`);
      }
    });
  });
  // v6.9 fix: 跨域导航时 window.__rpa_actions 会丢失
  // 在导航请求发出时（页面还没跳转），立即收集当前页面的 actions
  page.on('request', async (request) => {
    if (request.resourceType() !== 'document' || !request.isNavigationRequest()) return;
    // 排除初始加载（第一次 goto）
    if (actions.filter(a => a.type === 'navigate').length === 0) return;
    
    try {
      const pendingActions: any[] = await page.evaluate(() => {
        const acts = (window as any).__rpa_actions || [];
        (window as any).__rpa_actions = [];
        return acts;
      });
      if (pendingActions.length > 0) {
        for (const a of pendingActions) {
          actions.push({
            seqNum: ++seqCounter,
            timestamp: a.timestamp || Date.now(),
            relativeMs: (a.timestamp || Date.now()) - startTime,
            type: a.type,
            url: a.url || '',
            target: a.target,
            targetText: a.targetText,
            targetType: a.targetType,
            value: a.value,
            label: a.label,
            stabilityGrade: a.stabilityGrade,
            uniquenessMatch: a.uniquenessMatch,
            selectorStrategy: a.selectorStrategy,
            relatedApi: a.relatedApi,
          });
        }
        process.stdout.write(`  💾 [nav-save] 导航前抢救到 ${pendingActions.length} 个 actions（来自 ${request.url().substring(0, 60)}）\n`);
      }
    } catch {
      // 页面可能已经卸载，忽略
    }
  });

  page.on('framenavigated', (frame) => {
    if (frame !== page.mainFrame()) return;
    const url = frame.url();
    actions.push({ seqNum: ++seqCounter, timestamp: Date.now(), relativeMs: Date.now() - startTime, type: 'navigate', url, label: url });
    process.stdout.write(`  ↗  ${url.substring(0, 100)}\n`);
  });

  // ── Download event tracking (v6.5 + v7.5.0 实时保存) ────────────────────────
  // saveDownloadAndExtractHeaders 已在前面定义（供所有页面共用）
  page.on('download', async (download) => {
    try {
      const savedInfo = await saveDownloadAndExtractHeaders(download);
      downloadEvents.push({
        timestamp: Date.now(),
        relativeMs: Date.now() - startTime,
        url: download.url(),
        suggestedFilename: download.suggestedFilename(),
        mimeType: '',
        ...savedInfo,
      });
      process.stdout.write(`  📥 Download: ${download.suggestedFilename()}\n`);
    } catch (err) {
      process.stdout.write(`  ⚠️ Download event error: ${err}\n`);
    }
  });

  // ── Open initial URL ───────────────────────────────────────────────────────
  const startUrl = opts.ssoUrl || opts.appUrl;
  if (startUrl) {
    console.log(`🔗 Opening: ${startUrl}\n`);
    await page.goto(startUrl, { waitUntil: 'domcontentloaded', timeout: 30_000 }).catch(() => {});
  }

  // ── Interactive control ────────────────────────────────────────────────────
  console.log('─'.repeat(60));
  console.log('📋  Controls:');
  console.log('    Enter          → Add a marker (annotate what you did)');
  console.log('    done + Enter   → Stop recording and save');
  console.log('    Ctrl+C         → Emergency stop and save');
  console.log('─'.repeat(60));
  console.log('💡  Now perform your task in the browser.\n');

  const rl = readline.createInterface({ input: process.stdin, terminal: false });

  // 文件监控：检测 .done 文件（解决 PTY 模式下 stdin 无法传递的问题）
  const doneFilePath = path.join(outputDir, '.done');
  const stopRecordingFilePath = path.join(outputDir, '.stop');

  await new Promise<void>((resolve) => {
    let resolved = false;
    const safeResolve = () => { if (!resolved) { resolved = true; resolve(); } };

    rl.on('line', async (line) => {
      const input = line.trim().toLowerCase();
      if (input === 'done' || input === 'q' || input === 'exit') { console.log('\n⏹  Stopping recording...'); safeResolve(); return; }
      const label = line.trim() || `Marker at ${new Date().toISOString()}`;
      actions.push({ seqNum: ++seqCounter, timestamp: Date.now(), relativeMs: Date.now() - startTime, type: 'marker', url: page.url(), label });
      console.log(`  📌 Marker: "${label}"`);
    });
    rl.on('close', safeResolve);
    process.on('SIGINT', () => { console.log('\n⚠️  Interrupted - saving recording...'); safeResolve(); });

    // 文件监控：每 500ms 检查 .done 或 .stop 文件
    const fileCheckInterval = setInterval(() => {
      if (fs.existsSync(doneFilePath) || fs.existsSync(stopRecordingFilePath)) {
        console.log('\n⏹  Detected stop file, saving recording...');
        try { fs.unlinkSync(doneFilePath); } catch {}
        try { fs.unlinkSync(stopRecordingFilePath); } catch {}
        clearInterval(fileCheckInterval);
        safeResolve();
      }
    }, 500);
  });

  // ── Collect final state ────────────────────────────────────────────────────
  process.stdout.write('\n⏳  Collecting final browser state...\n');

  // v8.1.0: 强制处理完异步分析队列
  process.stdout.write('  🔄 Flushing async analysis queue...\n');
  await page.evaluate(() => {
    if (typeof (window as any).flushAnalysisQueue === 'function') {
      (window as any).flushAnalysisQueue();
    }
  });

  // ── Collect actions from ALL frames (main + iframes) ──
  const allFrames = page.frames();
  process.stdout.write(`  📦 Found ${allFrames.length} frame(s) to collect actions from...\n`);
  for (const frame of allFrames) {
    const isMainFrame = frame === page.mainFrame();
    const frameUrl = frame.url();
    try {
      const injectedActions: any[] = await frame.evaluate(() => (window as any).__rpa_actions || []);
      if (injectedActions.length > 0 && !isMainFrame) {
        process.stdout.write(`  📦 Collected ${injectedActions.length} actions from iframe: ${frameUrl.substring(0, 80)}\n`);
      }
      for (const a of injectedActions) {
        // Mark iframe actions
        if (!isMainFrame) {
          a.inIframe = true;
          a.frameUrl = frameUrl;
        }
        actions.push({ seqNum: ++seqCounter, timestamp: a.timestamp, relativeMs: a.timestamp - startTime, ...a });
      }
    } catch (err) {
      // Cross-origin iframes may throw — skip silently
      if (!isMainFrame) {
        process.stdout.write(`  ⚠️  Cannot access iframe (cross-origin?): ${frameUrl.substring(0, 80)}\n`);
      }
    }
  }
  actions.sort((a, b) => a.timestamp - b.timestamp);

  // ── Action-API correlation (match actions to nearby API calls) ─────────────
  process.stdout.write('🔗 Correlating actions with API calls...\n');
  const API_WINDOW_MS = 2000;  // Match API calls within 2 seconds after action
  
  // v7.2: 检测周期性 API（心跳/轮询/监控），同一 URL 出现 3+ 次视为周期性
  // 通用方案：不硬编码特定 URL，而是根据频率自动识别
  const apiUrlCounts: Record<string, number> = {};
  for (const r of requests) {
    if (['POST', 'PUT', 'PATCH'].includes(r.method)) {
      apiUrlCounts[r.url] = (apiUrlCounts[r.url] || 0) + 1;
    }
  }
  const periodicApiUrls = new Set(
    Object.entries(apiUrlCounts).filter(([_, count]) => count >= 3).map(([url]) => url)
  );
  if (periodicApiUrls.size > 0) {
    process.stdout.write(`  🔄 Detected ${periodicApiUrls.size} periodic API(s) (excluded from correlation):\n`);
    Array.from(periodicApiUrls).forEach(url => {
      process.stdout.write(`     ${url.substring(0, 80)} (${apiUrlCounts[url]}x)\n`);
    });
  }
  
  // Include all event types that can trigger API calls
  const API_TRIGGERING_EVENTS = new Set(['click', 'submit', 'keydown', 'drag', 'upload', 'scroll', 'dblclick', 'mouseenter', 'focus', 'blur']);
  for (const action of actions) {
    if (!API_TRIGGERING_EVENTS.has(action.type)) continue;
    // Find POST/PUT/PATCH requests within API_WINDOW_MS after this action
    const nearbyApis = requests.filter(r => {
      if (!['POST', 'PUT', 'PATCH'].includes(r.method)) return false;
      // v7.2: 排除周期性 API
      if (periodicApiUrls.has(r.url)) return false;
      const timeDiff = r.timestamp - action.timestamp;
      return timeDiff > 0 && timeDiff < API_WINDOW_MS;
    });
    if (nearbyApis.length > 0) {
      // Pick the closest API call
      const closest = nearbyApis.reduce((a, b) => 
        Math.abs(a.timestamp - action.timestamp) < Math.abs(b.timestamp - action.timestamp) ? a : b
      );
      action.relatedApi = `${closest.method} ${closest.url}`;
    }
  }

  // ── Detect conditional rendering (elements that appear after prior actions) ─
  // Fix #7: Improved logic - check if this is the FIRST time we see this target
  // An element is "conditionally rendered" if:
  // 1. It's the first time we interact with this selector
  // 2. It appeared shortly after a triggering action (click/select/submit/scroll)
  
  const seenTargets = new Set<string>();  // Track targets we've seen before
  const CONDITIONAL_RENDER_WINDOW_MS = 2000;  // Increased from 1000ms for slow pages
  
  for (let i = 0; i < actions.length; i++) {
    const curr = actions[i];
    if (curr.type !== 'click' && curr.type !== 'input' && curr.type !== 'select') continue;
    if (!curr.target) continue;
    
    const isFirstSighting = !seenTargets.has(curr.target);
    seenTargets.add(curr.target);
    
    if (isFirstSighting) {
      // Find the most recent triggering action before this one
      const prevTriggerAction = actions.slice(0, i).reverse().find(a => 
        a.type === 'click' || a.type === 'select' || a.type === 'submit' || a.type === 'scroll'
      );
      
      if (prevTriggerAction && curr.timestamp - prevTriggerAction.timestamp < CONDITIONAL_RENDER_WINDOW_MS) {
        // This element appeared for the first time shortly after a triggering action
        curr.appearsAfterAction = true;
        curr.dependsOnAction = prevTriggerAction.seqNum;
      }
    }
  }

  const finalCookies = await context.cookies();
  let finalLocalStorage: Record<string, string> = {};
  let finalSessionStorage: Record<string, string> = {};
  try {
    finalLocalStorage = await page.evaluate(() => { const d: Record<string, string> = {}; for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i)!; d[k] = localStorage.getItem(k)!; } return d; });
    finalSessionStorage = await page.evaluate(() => { const d: Record<string, string> = {}; for (let i = 0; i < sessionStorage.length; i++) { const k = sessionStorage.key(i)!; d[k] = sessionStorage.getItem(k)!; } return d; });
  } catch {}

  const endTime = Date.now();
  
  // ── Collect auth clues (for failure diagnosis) ──
  process.stdout.write('🔐 Collecting auth clues...\n');
  let authClues: AuthClues | undefined;
  try {
    authClues = await collectAuthClues(page, requests);
    process.stdout.write(`  📋 Auth type: ${authClues.authType}\n`);
    if (authClues.urlAuthParams.length > 0) {
      process.stdout.write(`  📋 URL auth params: ${authClues.urlAuthParams.map(p => p.name).join(', ')}\n`);
    }
    if (Object.keys(authClues.globalTokens).length > 0) {
      process.stdout.write(`  📋 Global tokens: ${Object.keys(authClues.globalTokens).join(', ')}\n`);
    }
    if (Object.keys(authClues.authHeaders).length > 0) {
      process.stdout.write(`  📋 Auth headers: ${Object.keys(authClues.authHeaders).join(', ')}\n`);
    }
  } catch (err: any) {
    process.stdout.write(`  ⚠️  Failed to collect auth clues: ${err.message}\n`);
  }

  // ── Download analysis (v6.5) ───────────────────────────────────────────────
  process.stdout.write('📥 Analyzing download events...\n');
  
  // 1. 关联下载事件到触发动作
  for (const dl of downloadEvents) {
    // 找到下载前 3 秒内最近的操作
    const triggerAction = actions.slice().reverse().find(a => 
      a.timestamp < dl.timestamp && 
      dl.timestamp - a.timestamp < 3000 &&
      ['click', 'submit', 'keydown'].includes(a.type)
    );
    if (triggerAction) {
      dl.triggerActionSeq = triggerAction.seqNum;
    }
  }
  
  // 2. 收集 DOM 变化信息
  let domChanges = { iframeCreated: false, iframeSrcs: [] as string[], blobUrlAnchors: false };
  try {
    domChanges = await page.evaluate(() => (window as any).__rpa_downloadDomChanges || domChanges);
  } catch {}
  
  // 3. 分析下载类型
  const downloadAnalysis: DownloadAnalysis = analyzeDownloadType(
    downloadEvents, 
    responses, 
    domChanges
  );
  
  if (downloadAnalysis.detected) {
    process.stdout.write(`  📋 Download type: ${downloadAnalysis.type} (${downloadAnalysis.confidence} confidence)\n`);
    if (downloadAnalysis.evidence.length > 0) {
      process.stdout.write(`  📋 Evidence: ${downloadAnalysis.evidence.join('; ')}\n`);
    }
  } else {
    process.stdout.write(`  📋 No download detected\n`);
  }

  // ── v7.4.3: 提取下载文件的表头（用于后续 API 模式校验）────────────────────
  // ── v7.5.0: 从实时保存的下载文件中提取表头 + 构建 downloadedFiles ──────────
  let downloadedFileHeaders: string[] | null = null;
  let downloadedFileName: string | null = null;
  const downloadedFiles: DownloadedFile[] = [];

  if (downloadEvents.length > 0) {
    process.stdout.write(`📊 Processing ${downloadEvents.length} downloaded file(s)...\n`);
    
    for (let i = 0; i < downloadEvents.length; i++) {
      const dl = downloadEvents[i];
      const fileIndex = i + 1;
      
      if (dl.savedPath && fs.existsSync(dl.savedPath)) {
        // 文件已在录制时保存，直接使用
        const fileName = dl.suggestedFilename || path.basename(dl.savedPath);
        downloadedFiles.push({
          index: fileIndex,
          fileName,
          savedPath: dl.savedPath,
          fileSize: dl.fileSize || 0,
          headers: dl.headers || null,
          downloadUrl: dl.url,
          triggerActionSeq: dl.triggerActionSeq,
          relatedRequestIds: dl.relatedRequestIds || [],
          timestamp: dl.timestamp,
        });
        
        // 兼容旧字段：取第一个文件的表头和文件名
        if (i === 0) {
          downloadedFileHeaders = dl.headers || null;
          downloadedFileName = fileName;
        }
        
        process.stdout.write(`  ✅ [${fileIndex}/${downloadEvents.length}] ${fileName} (${((dl.fileSize || 0) / 1024).toFixed(1)} KB, ${dl.headers?.length || 0} columns)\n`);
      } else {
        // fallback：文件未保存（可能是旧版本或异常情况），尝试从 Downloads 目录找
        process.stdout.write(`  ⚠️ [${fileIndex}/${downloadEvents.length}] File not saved, trying Downloads fallback...\n`);
        try {
          const userHome = process.env.USERPROFILE || process.env.HOME || '';
          const downloadsDir = path.join(userHome, 'Downloads');
          if (fs.existsSync(downloadsDir)) {
            const now = Date.now();
            const files = fs.readdirSync(downloadsDir);
            const recentFiles = files
              .filter(f => /\.(xlsx|xls|xlsm|csv|tsv)$/i.test(f))
              .map(f => {
                const filePath = path.join(downloadsDir, f);
                const stat = fs.statSync(filePath);
                return { name: f, path: filePath, mtime: stat.mtimeMs };
              })
              .filter(f => now - f.mtime < 5 * 60 * 1000)
              .sort((a, b) => b.mtime - a.mtime);
            
            if (recentFiles.length > 0) {
              const latestFile = recentFiles[0];
              downloadedFiles.push({
                index: fileIndex,
                fileName: latestFile.name,
                savedPath: latestFile.path,
                fileSize: fs.statSync(latestFile.path).size,
                headers: null, // TODO: 提取表头
                downloadUrl: dl.url,
                triggerActionSeq: dl.triggerActionSeq,
                relatedRequestIds: dl.relatedRequestIds || [],
                timestamp: dl.timestamp,
              });
              if (i === 0) {
                downloadedFileName = latestFile.name;
              }
              process.stdout.write(`  📄 Fallback found: ${latestFile.name}\n`);
            }
          }
        } catch (err: any) {
          process.stdout.write(`  ⚠️ Fallback failed: ${err.message}\n`);
        }
      }
    }
    
    if (downloadedFiles.length > 0) {
      process.stdout.write(`  📊 Total: ${downloadedFiles.length} file(s) saved\n`);
      
      // v7.5.0: 根据 periodicApiUrls 过滤掉轮询请求的关联
      if (periodicApiUrls.size > 0) {
        for (const file of downloadedFiles) {
          const beforeCount = file.relatedRequestIds.length;
          file.relatedRequestIds = file.relatedRequestIds.filter(reqId => {
            const req = requests.find(r => r.id === reqId);
            if (!req) return false;
            return !periodicApiUrls.has(req.url.split('?')[0]);
          });
          if (file.relatedRequestIds.length < beforeCount) {
            process.stdout.write(`  🔧 [${file.index}] Filtered ${beforeCount - file.relatedRequestIds.length} polling request(s)\n`);
          }
        }
      }
    }
  }

  // 4. 收集 DOM 变化到 actions（如果有 iframe/blob 创建）
  if (domChanges.iframeCreated || domChanges.blobUrlAnchors) {
    actions.push({
      seqNum: ++seqCounter,
      timestamp: Date.now(),
      relativeMs: Date.now() - startTime,
      type: 'marker',
      url: page.url(),
      label: `[download-dom] iframe:${domChanges.iframeCreated} blob:${domChanges.blobUrlAnchors}`,
    });
  }

  // ── v7.2: Download chain & polling detection ─────────────────────────────
  process.stdout.write('🔗 Detecting download chains & polling patterns...\n');
  
  const downloadChains = detectDownloadChains(requests, responses, downloadEvents, actions);
  const pollingPatterns = detectPollingPatterns(requests);
  
  if (downloadChains.length > 0) {
    for (const chain of downloadChains) {
      process.stdout.write(`  🔗 Chain: ${chain.exportUrl.substring(chain.exportUrl.lastIndexOf('/') + 1, chain.exportUrl.lastIndexOf('/') + 40)} → ${chain.downloadUrl.substring(chain.downloadUrl.lastIndexOf('/') + 1, chain.downloadUrl.lastIndexOf('/') + 40)} (${chain.betweenRequests.length} intermediate requests, ${chain.gapMs}ms gap)\n`);
      // v7.3: Bridge evidence
      if (chain.bridgeEvidence) {
        if (chain.bridgeEvidence.found) {
          process.stdout.write(`  ✅ Bridge: "${chain.bridgeEvidence.matchValue?.substring(0, 40)}..." found in intermediate response\n`);
        } else {
          process.stdout.write(`  ❌ Bridge: download param not found in intermediate responses (need manual analysis)\n`);
        }
      }
    }
  } else {
    process.stdout.write(`  🔗 No download chains detected\n`);
  }
  
  if (pollingPatterns.length > 0) {
    for (const pattern of pollingPatterns) {
      process.stdout.write(`  🔄 Polling: ${pattern.method} ${pattern.urlPath} (${pattern.count} calls, avg ${pattern.avgIntervalMs}ms)\n`);
    }
  } else {
    process.stdout.write(`  🔄 No polling patterns detected\n`);
  }
  
  // ── v6.6: Data filtering (unless --save-full) ──────────────────────────────
  const saveFull = opts.saveFull;
  let filteredActions = actions;
  let filteredRequests = requests;
  
  if (!saveFull) {
    process.stdout.write('🔍 Filtering recording data...\n');
    
    // 1. Filter actions (remove useless events)
    const actionsBefore = actions.length;
    filteredActions = filterActions(actions);
    process.stdout.write(`  📋 Actions: ${actionsBefore} → ${filteredActions.length} (filtered ${actionsBefore - filteredActions.length})\n`);
    
    // 2. Filter request headers (keep only essential ones)
    const authHeaderNames = authClues ? Object.keys(authClues.authHeaders) : [];
    for (const req of requests) {
      req.headers = filterHeaders(req.headers, authHeaderNames);
    }
    process.stdout.write(`  📋 Request headers: filtered (kept essential + auth headers)\n`);
  } else {
    process.stdout.write('💾 Save full mode: no filtering applied\n');
  }
  
  // ── Build recording object ─────────────────────────────────────────────────
  const recording: Recording = { 
    version: '1.0', taskName, startTime, endTime, durationMs: endTime - startTime, 
    ssoUrl: opts.ssoUrl || '', finalUrl: page.url(), 
    requests: filteredRequests, responses, actions: filteredActions, 
    // v6.6: only save cookies/storage in --save-full mode
    finalCookies: saveFull ? finalCookies : [],
    finalLocalStorage: saveFull ? finalLocalStorage : {},
    finalSessionStorage: saveFull ? finalSessionStorage : {},
    notes, authClues,
    downloadEvents,      // v6.5
    downloadAnalysis,    // v6.5
    downloadChains,      // v7.2
    pollingPatterns,     // v7.2
    downloadedFileHeaders,  // v7.4.3: 下载文件的表头（用于 API 模式校验）
    downloadedFileName,     // v7.4.3: 下载文件名
    downloadedFiles,        // v7.5.0: 所有下载文件的完整信息
  };

  // ── Save ───────────────────────────────────────────────────────────────────
  // v7.4.1: 关闭 bodies 文件写入流
  bodiesStream.end();
  
  // v8.4.1: 先写临时文件再 rename，防止写入中断导致数据丢失
  const recordingPath = path.join(outputDir, 'recording.json');
  const recordingTmpPath = recordingPath + '.tmp';
  fs.writeFileSync(recordingTmpPath, JSON.stringify(recording, null, 2));
  fs.renameSync(recordingTmpPath, recordingPath);
  // ── v8.5.0: 列出全部请求（不过滤，让AI在分析阶段自己判断）──────────────
  // 简单分两组：API请求（xhr/fetch）和 静态资源
  const apiRequests = filteredRequests.filter(r => r.resourceType === 'xhr' || r.resourceType === 'fetch');
  const staticRequests = filteredRequests.filter(r => r.resourceType !== 'xhr' && r.resourceType !== 'fetch');

  // ── 生成接口清单文件 ──────────────────────────────────────────────
  // 目的：列出全部接口，避免过滤导致漏掉核心接口
  // 阶段三直接读取此文件，AI会自己分析接口的重要性和调用关系
  const apiListLines = [
    '# 接口清单',
    '',
    `> 录制时间：${new Date(startTime).toISOString()}`,
    `> API请求：${apiRequests.length} 个`,
    `> 静态资源：${staticRequests.length} 个`,
    '',
    '## API请求（xhr/fetch）',
    '',
    '| # | Method | URL | Status | Body完整 | 说明 |',
    '|---|--------|-----|--------|----------|------|',
  ];
  
  apiRequests.forEach((r, idx) => {
    const resp = responses[r.id];
    const status = resp ? resp.status : '?';
    const bodyFull = resp?.bodySaved ? '✅' : (resp?.bodySummary ? '📋' : '❓');
    const bodyNote = resp?.bodySaved ? '有完整body' : (resp?.bodySummary ? '仅摘要，完整数据在recording-bodies.jsonl' : '无body');
    apiListLines.push(`| ${idx + 1} | ${r.method} | ${r.url} | ${status} | ${bodyFull} | ${bodyNote} |`);
  });
  
  // 静态资源只列URL，不展开
  if (staticRequests.length > 0) {
    apiListLines.push(
      '',
      `## 静态资源（${staticRequests.length} 个，通常可忽略）`,
      '',
      '| # | Method | URL | Type |',
      '|---|--------|-----|------|',
    );
    staticRequests.forEach((r, idx) => {
      apiListLines.push(`| ${idx + 1} | ${r.method} | ${r.url} | ${r.resourceType || '?'} |`);
    });
  }
  
  apiListLines.push(
    '',
    '## Body完整性说明',
    '',
    '- ✅ = 有完整body（可直接分析）',
    '- 📋 = 仅摘要（完整数据在 `recording-bodies.jsonl`，按 requestId 查找）',
    '- ❓ = 无body（可能是GET请求或响应解析失败）',
    '',
    '## 提取完整接口数据的方法',
    '',
    '```powershell',
    '# 提取某个接口的完整请求体',
    'node -e "const d=JSON.parse(require(\'fs\').readFileSync(\'recording.json\'));',
    'const r=d.requests.find(x=>x.id===\'req_0001\');console.log(r.postData);"',
    '',
    '# 提取某个接口的完整响应体（如果只有摘要）',
    'node -e "const lines=require(\'fs\').readFileSync(\'recording-bodies.jsonl\',\'utf8\').split(\'\\n\');',
    'const r=JSON.parse(lines.find(l=>l.includes(\'req_0001\')));console.log(r.body);"',
    '```'
  );
  
  fs.writeFileSync(path.join(outputDir, 'api-list.md'), apiListLines.join('\n'));

  // ── Calculate file size ──
  const recordingSize = fs.statSync(path.join(outputDir, 'recording.json')).size;

  // v8.4.1: try-finally 确保异常时也能关闭浏览器
  try {
    console.log('\n✅  Recording complete!');
    console.log(`    ${filteredRequests.length} requests | ${apiRequests.length} APIs | ${staticRequests.length} static | ${filteredActions.length} actions`);
    console.log(`    File size: ${(recordingSize / 1024).toFixed(1)} KB (${saveFull ? 'full mode' : 'filtered mode'})`);
    console.log(`    Saved to: ${outputDir}`);
    console.log(`    API list: ${path.join(outputDir, 'api-list.md')}`);
    console.log(`\n📊  Next step:`);
    console.log(`    Tell me to analyze the recording at: ${outputDir}\n`);
  } finally {
    await context.close();
    await browser.close();
  }
}

main().catch(err => { console.error('\n❌ Fatal error:', err.message); process.exit(1); });
