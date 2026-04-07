import type { EditorConfig } from 'grapesjs'

export function buildGrapesConfig(_pageId: number): EditorConfig {
  return {
    container: '#gjs',
    fromElement: false,
    height: '100%',
    width: 'auto',
    storageManager: {
      type: 'backend',
      autosave: false,
      autoload: true,
    },
    assetManager: {
      assets: [],
      upload: false, // handled by our custom panel
    },
    blockManager: {
      appendTo: '#blocks-panel',
    },
    styleManager: {
      appendTo: '#styles-panel',
      sectors: [
        {
          name: 'General',
          open: true,
          properties: [
            { name: 'Float', property: 'float', type: 'radio', defaults: 'none', list: [{ id: 'none', value: 'none', className: 'fa fa-times' }, { id: 'left', value: 'left', className: 'fa fa-align-left' }, { id: 'right', value: 'right', className: 'fa fa-align-right' }] },
            'display', 'position', 'top', 'right', 'left', 'bottom',
          ],
        },
        {
          name: 'Dimension',
          open: false,
          properties: ['width', 'height', 'max-width', 'min-height', 'margin', 'padding'],
        },
        {
          name: 'Typography',
          open: false,
          properties: ['font-family', 'font-size', 'font-weight', 'letter-spacing', 'color', 'line-height', 'text-align', 'text-decoration', 'text-shadow'],
        },
        {
          name: 'Decorations',
          open: false,
          properties: ['opacity', 'background-color', 'border-radius', 'border', 'box-shadow', 'background'],
        },
        {
          name: 'Extra',
          open: false,
          properties: ['transition', 'transform'],
        },
      ],
    },
    layerManager: {
      appendTo: '#layers-panel',
    },
    traitManager: {
      appendTo: '#traits-panel',
    },
    deviceManager: {
      devices: [
        { name: 'Desktop', width: '' },
        { name: 'Tablet', width: '768px', widthMedia: '992px' },
        { name: 'Mobile', width: '320px', widthMedia: '480px' },
      ],
    },
    canvas: {
      styles: [
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap',
      ],
      scripts: [],
    },
    panels: { defaults: [] }, // We build custom panels in BuilderPage
  }
}
