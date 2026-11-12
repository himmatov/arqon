// Usage: node render.js [out.mp4] [fps]   |  node render.js --stills t1,t2,...
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const args = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto('file://' + path.resolve(__dirname, 'animation.html') + '#render');
  await page.evaluate(() => document.fonts.ready);
  const grab = (t, type) => page.evaluate(([t, type]) => { render(t); return document.getElementById('c').toDataURL(type, 0.95); }, [t, type]);
  if (args[0] === '--stills') {
    const fs = require('fs'); const dir = args[2] || 'stills'; fs.mkdirSync(dir, { recursive: true });
    for (const t of args[1].split(',').map(Number)) {
      const d = await grab(t, 'image/jpeg');
      fs.writeFileSync(`${dir}/t${String(t).padStart(5, '0')}.jpg`, Buffer.from(d.split(',')[1], 'base64'));
    }
    await browser.close(); return;
  }
  const out = args[0] || 'menga-consulting-koreya.mp4';
  const fps = Number(args[1] || 30);
  const dur = await page.evaluate(() => DURATION);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const total = Math.round(dur * fps);
  for (let i = 0; i < total; i++) {
    const d = await grab(i / fps, 'image/jpeg');
    if (!ff.stdin.write(Buffer.from(d.split(',')[1], 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 150 === 0) console.log(`frame ${i}/${total}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log('done ->', out);
})();
