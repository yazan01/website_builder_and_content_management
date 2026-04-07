import type { Editor } from 'grapesjs'

export function registerBlocks(editor: Editor) {
  const bm = editor.BlockManager

  // --- Layout ---
  bm.add('section', {
    label: 'Section',
    category: 'Layout',
    content: '<section class="py-16 px-8"><div class="max-w-6xl mx-auto"></div></section>',
    media: `<svg viewBox="0 0 24 24"><rect x="2" y="6" width="20" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>`,
  })

  bm.add('container', {
    label: 'Container',
    category: 'Layout',
    content: '<div class="max-w-6xl mx-auto px-4"></div>',
    media: `<svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>`,
  })

  bm.add('2-columns', {
    label: '2 Columns',
    category: 'Layout',
    content: '<div style="display:flex;gap:16px"><div style="flex:1;min-height:60px;padding:8px;border:1px dashed #ccc"></div><div style="flex:1;min-height:60px;padding:8px;border:1px dashed #ccc"></div></div>',
    media: `<svg viewBox="0 0 24 24"><rect x="2" y="6" width="9" height="12" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/><rect x="13" y="6" width="9" height="12" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>`,
  })

  bm.add('3-columns', {
    label: '3 Columns',
    category: 'Layout',
    content: '<div style="display:flex;gap:12px"><div style="flex:1;min-height:60px;padding:8px;border:1px dashed #ccc"></div><div style="flex:1;min-height:60px;padding:8px;border:1px dashed #ccc"></div><div style="flex:1;min-height:60px;padding:8px;border:1px dashed #ccc"></div></div>',
    media: `<svg viewBox="0 0 24 24"><rect x="1" y="7" width="6" height="10" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/><rect x="9" y="7" width="6" height="10" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/><rect x="17" y="7" width="6" height="10" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>`,
  })

  // --- Typography ---
  bm.add('heading', {
    label: 'Heading',
    category: 'Typography',
    content: '<h2 style="font-size:2rem;font-weight:700;margin:0">Your Heading</h2>',
    media: `<svg viewBox="0 0 24 24"><text x="3" y="17" font-size="14" font-weight="bold" fill="currentColor">H1</text></svg>`,
  })

  bm.add('text', {
    label: 'Text',
    category: 'Typography',
    content: '<p style="line-height:1.6;margin:0">Write your text here. Click to edit this paragraph.</p>',
    media: `<svg viewBox="0 0 24 24"><line x1="3" y1="6" x2="21" y2="6" stroke="currentColor" stroke-width="1.5"/><line x1="3" y1="10" x2="21" y2="10" stroke="currentColor" stroke-width="1.5"/><line x1="3" y1="14" x2="17" y2="14" stroke="currentColor" stroke-width="1.5"/></svg>`,
  })

  bm.add('quote', {
    label: 'Quote',
    category: 'Typography',
    content: '<blockquote style="border-left:4px solid #3b82f6;padding:12px 20px;margin:0;background:#f8fafc;font-style:italic;color:#475569">"Your inspiring quote goes here."</blockquote>',
    media: `<svg viewBox="0 0 24 24"><path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>`,
  })

  // --- Media ---
  bm.add('image', {
    label: 'Image',
    category: 'Media',
    content: { type: 'image', style: { maxWidth: '100%' } },
    media: `<svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="8.5" cy="8.5" r="1.5" fill="currentColor"/><path d="M21 15l-5-5L5 21" stroke="currentColor" stroke-width="1.5" fill="none"/></svg>`,
  })

  bm.add('video', {
    label: 'Video',
    category: 'Media',
    content: { type: 'video', src: '', style: { width: '100%', height: '315px' } },
    media: `<svg viewBox="0 0 24 24"><rect x="2" y="6" width="15" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M17 9l5-3v12l-5-3V9z" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>`,
  })

  // --- UI Components ---
  bm.add('button', {
    label: 'Button',
    category: 'UI',
    content: '<a href="#" style="display:inline-block;padding:12px 28px;background:#3b82f6;color:#fff;border-radius:8px;text-decoration:none;font-weight:600;font-size:1rem">Click Me</a>',
    media: `<svg viewBox="0 0 24 24"><rect x="3" y="8" width="18" height="8" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>`,
  })

  bm.add('card', {
    label: 'Card',
    category: 'UI',
    content: `<div style="border:1px solid #e2e8f0;border-radius:12px;overflow:hidden;max-width:320px;box-shadow:0 1px 3px rgba(0,0,0,.1)">
  <img src="https://placehold.co/320x200" alt="Card image" style="width:100%;display:block"/>
  <div style="padding:20px">
    <h3 style="margin:0 0 8px;font-size:1.125rem;font-weight:600">Card Title</h3>
    <p style="margin:0 0 16px;color:#64748b;font-size:.875rem">Card description goes here. Add your content.</p>
    <a href="#" style="display:inline-block;padding:8px 20px;background:#3b82f6;color:#fff;border-radius:6px;text-decoration:none;font-size:.875rem;font-weight:500">Learn More</a>
  </div>
</div>`,
    media: `<svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/><line x1="3" y1="10" x2="21" y2="10" stroke="currentColor" stroke-width="1.5"/></svg>`,
  })

  bm.add('hero', {
    label: 'Hero Section',
    category: 'UI',
    content: `<section style="padding:80px 32px;background:linear-gradient(135deg,#1e293b,#3b82f6);text-align:center;color:#fff">
  <h1 style="font-size:3rem;font-weight:800;margin:0 0 16px">Welcome to Your Site</h1>
  <p style="font-size:1.25rem;margin:0 0 32px;opacity:.9">Build beautiful websites with our drag & drop editor</p>
  <a href="#" style="display:inline-block;padding:14px 36px;background:#fff;color:#1e293b;border-radius:8px;text-decoration:none;font-weight:700;font-size:1rem">Get Started</a>
</section>`,
    media: `<svg viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/><line x1="8" y1="21" x2="16" y2="21" stroke="currentColor" stroke-width="1.5"/><line x1="12" y1="17" x2="12" y2="21" stroke="currentColor" stroke-width="1.5"/></svg>`,
  })

  bm.add('navbar', {
    label: 'Navbar',
    category: 'UI',
    content: `<nav style="display:flex;align-items:center;justify-content:space-between;padding:16px 32px;background:#1e293b;color:#fff">
  <div style="font-size:1.25rem;font-weight:700">Logo</div>
  <div style="display:flex;gap:24px">
    <a href="#" style="color:#cbd5e1;text-decoration:none;font-size:.9rem">Home</a>
    <a href="#" style="color:#cbd5e1;text-decoration:none;font-size:.9rem">About</a>
    <a href="#" style="color:#cbd5e1;text-decoration:none;font-size:.9rem">Services</a>
    <a href="#" style="color:#cbd5e1;text-decoration:none;font-size:.9rem">Contact</a>
  </div>
</nav>`,
    media: `<svg viewBox="0 0 24 24"><rect x="2" y="4" width="20" height="4" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/><line x1="6" y1="6" x2="6" y2="6" stroke="currentColor" stroke-width="2"/><line x1="14" y1="6" x2="18" y2="6" stroke="currentColor" stroke-width="1.5"/></svg>`,
  })

  bm.add('footer', {
    label: 'Footer',
    category: 'UI',
    content: `<footer style="background:#0f172a;color:#94a3b8;padding:40px 32px;text-align:center">
  <p style="margin:0 0 8px;font-size:.875rem">© 2025 Your Company. All rights reserved.</p>
  <div style="display:flex;gap:16px;justify-content:center">
    <a href="#" style="color:#64748b;text-decoration:none;font-size:.8rem">Privacy</a>
    <a href="#" style="color:#64748b;text-decoration:none;font-size:.8rem">Terms</a>
    <a href="#" style="color:#64748b;text-decoration:none;font-size:.8rem">Contact</a>
  </div>
</footer>`,
    media: `<svg viewBox="0 0 24 24"><rect x="2" y="16" width="20" height="4" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>`,
  })

  // --- Forms ---
  bm.add('form', {
    label: 'Contact Form',
    category: 'Forms',
    content: `<form style="max-width:480px;padding:32px;border:1px solid #e2e8f0;border-radius:12px">
  <h3 style="margin:0 0 20px;font-size:1.25rem;font-weight:600">Contact Us</h3>
  <div style="margin-bottom:16px">
    <label style="display:block;margin-bottom:6px;font-size:.875rem;font-weight:500;color:#374151">Name</label>
    <input type="text" placeholder="Your name" style="width:100%;padding:10px 12px;border:1px solid #d1d5db;border-radius:6px;font-size:.875rem;box-sizing:border-box"/>
  </div>
  <div style="margin-bottom:16px">
    <label style="display:block;margin-bottom:6px;font-size:.875rem;font-weight:500;color:#374151">Email</label>
    <input type="email" placeholder="your@email.com" style="width:100%;padding:10px 12px;border:1px solid #d1d5db;border-radius:6px;font-size:.875rem;box-sizing:border-box"/>
  </div>
  <div style="margin-bottom:20px">
    <label style="display:block;margin-bottom:6px;font-size:.875rem;font-weight:500;color:#374151">Message</label>
    <textarea rows="4" placeholder="Your message" style="width:100%;padding:10px 12px;border:1px solid #d1d5db;border-radius:6px;font-size:.875rem;resize:vertical;box-sizing:border-box"></textarea>
  </div>
  <button type="submit" style="width:100%;padding:12px;background:#3b82f6;color:#fff;border:none;border-radius:6px;font-size:1rem;font-weight:600;cursor:pointer">Send Message</button>
</form>`,
    media: `<svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" fill="none" stroke="currentColor" stroke-width="1.5"/><line x1="7" y1="9" x2="17" y2="9" stroke="currentColor" stroke-width="1.5"/><line x1="7" y1="13" x2="17" y2="13" stroke="currentColor" stroke-width="1.5"/><line x1="7" y1="17" x2="13" y2="17" stroke="currentColor" stroke-width="1.5"/></svg>`,
  })

  bm.add('divider', {
    label: 'Divider',
    category: 'UI',
    content: '<hr style="border:none;border-top:1px solid #e2e8f0;margin:24px 0"/>',
    media: `<svg viewBox="0 0 24 24"><line x1="3" y1="12" x2="21" y2="12" stroke="currentColor" stroke-width="1.5"/></svg>`,
  })
}
