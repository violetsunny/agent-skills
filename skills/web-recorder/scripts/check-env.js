#!/usr/bin/env node
/**
 * 网页录制技能 - 环境检查脚本（纯 JS 版本）
 * 
 * 只需要 Node.js 就能运行，不需要 ts-node
 * 
 * 检查项：
 * 1. Node.js 版本
 * 2. npm 依赖是否安装（缺失则自动安装）
 * 3. Chrome 浏览器是否存在
 * 
 * 退出码：0=全部通过，1=有缺失且无法自动修复
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const http = require('http');

const SKILL_DIR = path.resolve(__dirname, '..');
const NODE_MODULES = path.join(SKILL_DIR, 'node_modules');

// 颜色输出
const green = (s) => `\x1b[32m${s}\x1b[0m`;
const red = (s) => `\x1b[31m${s}\x1b[0m`;
const yellow = (s) => `\x1b[33m${s}\x1b[0m`;
const cyan = (s) => `\x1b[36m${s}\x1b[0m`;

let autoFixed = false;

function log(msg) {
  console.log(msg);
}

function checkNodeVersion() {
  log(cyan('📦 检查 Node.js 版本...'));
  try {
    const version = process.version;
    const major = parseInt(version.slice(1).split('.')[0]);
    if (major < 18) {
      log(red(`  ❌ Node.js 版本过低: ${version}，需要 >= 18`));
      return false;
    }
    log(green(`  ✅ Node.js ${version}`));
    return true;
  } catch {
    log(red('  ❌ 无法获取 Node.js 版本'));
    return false;
  }
}

function checkNpmDependencies() {
  log(cyan('\n📦 检查 npm 依赖...'));
  
  if (!fs.existsSync(NODE_MODULES)) {
    log(yellow('  ⚠️ node_modules 不存在，正在安装...'));
    try {
      execSync('npm install', { cwd: SKILL_DIR, stdio: 'inherit' });
      log(green('  ✅ npm 依赖安装完成'));
      autoFixed = true;
      return true;
    } catch (err) {
      log(red('  ❌ npm install 失败'));
      return false;
    }
  }
  
  // 检查关键依赖是否存在
  const keyDeps = ['playwright', 'ts-node', 'exceljs'];
  const missing = keyDeps.filter(dep => !fs.existsSync(path.join(NODE_MODULES, dep)));
  
  if (missing.length > 0) {
    log(yellow(`  ⚠️ 缺少依赖: ${missing.join(', ')}，正在安装...`));
    try {
      execSync('npm install', { cwd: SKILL_DIR, stdio: 'inherit' });
      log(green('  ✅ npm 依赖安装完成'));
      autoFixed = true;
      return true;
    } catch {
      log(red('  ❌ npm install 失败'));
      return false;
    }
  }
  
  log(green('  ✅ npm 依赖完整'));
  return true;
}

const readline = require('readline');

function checkChromeBrowser() {
  log(cyan('\n🔍 检查 Chrome 浏览器...'));
  
  const platform = process.platform;
  let chromePath = null;
  
  // 1. 优先检查环境变量
  if (process.env.CHROME_PATH && fs.existsSync(process.env.CHROME_PATH)) {
    chromePath = process.env.CHROME_PATH;
    log(green(`  ✅ 从环境变量找到: ${chromePath}`));
    return true;
  }
  
  // 2. 用系统命令查找
  try {
    if (platform === 'win32') {
      // Windows: 先尝试 where 命令
      try {
        const result = execSync('where chrome 2>nul', { encoding: 'utf-8' }).trim();
        if (result) {
          chromePath = result.split('\n')[0].trim();
        }
      } catch {
        // where 失败，继续尝试注册表
      }
      
      // 注册表查询（多个位置）
      if (!chromePath) {
        const regPaths = [
          'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\chrome.exe',
          'HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\chrome.exe',
        ];
        
        for (const regPath of regPaths) {
          try {
            const result = execSync(`reg query "${regPath}" /ve 2>nul`, { encoding: 'utf-8' });
            const match = result.match(/REG_SZ\s+(.+)/);
            if (match && fs.existsSync(match[1].trim())) {
              chromePath = match[1].trim();
              break;
            }
          } catch {
            // 注册表项不存在
          }
        }
      }
      
      // 常见路径（兜底）
      if (!chromePath) {
        const commonPaths = [
          `${process.env.ProgramFiles}\\Google\\Chrome\\Application\\chrome.exe`,
          `${process.env['ProgramFiles(x86)']}\\Google\\Chrome\\Application\\chrome.exe`,
          `${process.env.LOCALAPPDATA}\\Google\\Chrome\\Application\\chrome.exe`,
          `C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe`,
          `C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe`,
        ];
        
        for (const p of commonPaths) {
          if (p && fs.existsSync(p)) {
            chromePath = p;
            break;
          }
        }
      }
    } else if (platform === 'darwin') {
      // macOS
      const macPaths = [
        '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        `${process.env.HOME}/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`,
      ];
      
      for (const p of macPaths) {
        if (fs.existsSync(p)) {
          chromePath = p;
          break;
        }
      }
      
      // 尝试 which 命令
      if (!chromePath) {
        try {
          const result = execSync('which "google chrome" 2>/dev/null', { encoding: 'utf-8' }).trim();
          if (result) chromePath = result;
        } catch {}
      }
    } else {
      // Linux
      try {
        const result = execSync(
          'which google-chrome 2>/dev/null || which google-chrome-stable 2>/dev/null || which chromium-browser 2>/dev/null || which chromium 2>/dev/null',
          { encoding: 'utf-8' }
        ).trim();
        if (result) {
          chromePath = result.split('\n')[0].trim();
        }
      } catch {}
    }
  } catch {
    // 检查过程出错
  }
  
  // 最终判断
  if (chromePath && fs.existsSync(chromePath)) {
    log(green(`  ✅ Chrome 已安装: ${chromePath}`));
    return true;
  }
  
  return false;
}

async function installChrome() {
  log(cyan('\n📦 自动安装 Chrome...'));
  
  const platform = process.platform;
  
  try {
    if (platform === 'win32') {
      // Windows: 优先 winget，其次 choco
      try {
        execSync('winget --version', { stdio: 'ignore' });
        log(yellow('  → 使用 winget 安装...'));
        execSync('winget install --id Google.Chrome --accept-source-agreements --accept-package-agreements', { stdio: 'inherit' });
        log(green('  ✅ Chrome 安装完成'));
        return true;
      } catch {
        log(yellow('  → winget 不可用，尝试 Chocolatey...'));
      }
      
      try {
        execSync('choco --version', { stdio: 'ignore' });
        log(yellow('  → 使用 Chocolatey 安装...'));
        execSync('choco install googlechrome -y', { stdio: 'inherit' });
        log(green('  ✅ Chrome 安装完成'));
        return true;
      } catch {
        log(yellow('  → Chocolatey 不可用'));
      }
      
      // 都没有，下载安装包
      log(yellow('  → 正在下载 Chrome 安装包...'));
      const installerPath = path.join(process.env.TEMP || '.', 'ChromeSetup.exe');
      execSync(`curl -L -o "${installerPath}" "https://dl.google.com/chrome/install/latest/chrome_installer.exe"`, { stdio: 'inherit' });
      log(yellow(`  → 安装包已下载: ${installerPath}`));
      log(yellow('  → 请手动运行安装包完成安装'));
      return false;
      
    } else if (platform === 'darwin') {
      // macOS: 优先 brew
      try {
        execSync('brew --version', { stdio: 'ignore' });
        log(yellow('  → 使用 Homebrew 安装...'));
        execSync('brew install --cask google-chrome', { stdio: 'inherit' });
        log(green('  ✅ Chrome 安装完成'));
        return true;
      } catch {
        log(yellow('  → Homebrew 不可用'));
        log(yellow('  → 请手动下载安装: https://www.google.com/chrome/'));
        return false;
      }
      
    } else {
      // Linux: 尝试 apt
      try {
        execSync('which apt', { stdio: 'ignore' });
        log(yellow('  → 使用 apt 安装...'));
        execSync('sudo apt update && sudo apt install -y google-chrome-stable', { stdio: 'inherit' });
        log(green('  ✅ Chrome 安装完成'));
        return true;
      } catch {
        log(yellow('  → apt 不可用'));
        log(yellow('  → 请手动下载安装: https://www.google.com/chrome/'));
        return false;
      }
    }
  } catch (err) {
    log(red(`  ❌ 安装失败: ${err.message}`));
    return false;
  }
}

function askQuestion(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.trim().toLowerCase());
    });
  });
}

function checkCDPPort() {
  log(cyan('\n🔌 检查 CDP 端口 (18801)...'));
  
  return new Promise((resolve) => {
    const req = http.get('http://127.0.0.1:18801/json/version', (res) => {
      if (res.statusCode === 200) {
        log(green('  ✅ CDP 端口可用（浏览器已启动）'));
      } else {
        log(yellow('  ⚠️ CDP 端口响应异常（浏览器未启动，运行时会自动启动）'));
      }
      resolve(true);
    });
    req.on('error', () => {
      log(yellow('  ⚠️ CDP 端口未监听（浏览器未启动，运行时会自动启动）'));
      resolve(true);
    });
    req.setTimeout(3000, () => {
      req.destroy();
      log(yellow('  ⚠️ CDP 端口连接超时（浏览器未启动，运行时会自动启动）'));
      resolve(true);
    });
  });
}

async function main() {
  log(cyan('\n🔧 网页录制技能 - 环境检查\n'));
  log(`技能目录: ${SKILL_DIR}\n`);
  
  const results = {
    node: checkNodeVersion(),
    npm: checkNpmDependencies(),
    chrome: checkChromeBrowser(),
  };
  
  // Chrome 未安装时，询问用户是否自动安装
  if (!results.chrome) {
    log(red('\n⚠️  Chrome 未安装，录制功能将无法使用！'));
    log(yellow('   是否自动安装 Chrome？(y/n)'));
    
    const answer = await askQuestion('   请输入: ');
    
    if (answer === 'y' || answer === 'yes') {
      results.chrome = await installChrome();
      if (results.chrome) {
        autoFixed = true;
      }
    } else {
      log(yellow('\n   已取消安装。请手动安装 Chrome 后再使用录制功能。'));
      log(yellow('   下载地址: https://www.google.com/chrome/'));
    }
  }
  
  // 异步检查 CDP 端口
  await checkCDPPort();
  
  log('\n' + '─'.repeat(50));
  log(cyan('\n📊 检查结果汇总:\n'));
  
  const items = [
    ['Node.js', results.node],
    ['npm 依赖', results.npm],
    ['Chrome 浏览器', results.chrome],
  ];
  
  for (const [name, ok] of items) {
    log(`  ${ok ? green('✅') : red('❌')} ${name}`);
  }
  
  if (autoFixed) {
    log(yellow('\n⚡ 部分依赖已自动安装，可以开始录制了！'));
  }
  
  if (!results.node || !results.npm) {
    log(red('\n❌ 环境检查失败，请手动修复上述问题'));
    process.exit(1);
  }
  
  if (!results.chrome) {
    log(red('\n❌ Chrome 未安装，录制功能无法使用'));
    log(yellow('   请安装 Chrome 后重试'));
    process.exit(1);
  }
  
  log(green('\n✅ 环境检查通过，可以开始录制！\n'));
  process.exit(0);
}

main().catch(err => {
  log(red(`\n❌ 环境检查异常: ${err.message}`));
  process.exit(1);
});
