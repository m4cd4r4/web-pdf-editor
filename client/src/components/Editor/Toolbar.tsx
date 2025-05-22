import React from 'react';
import { usePDF } from '../../context/PDFContext';
import IconButton from '../common/IconButton';
import './Toolbar.css';

interface ToolbarProps {
  activeTool: string;
  onToolChange: (tool: string) => void;
  onToggleAIAssistant: () => void;
}

const Toolbar: React.FC<ToolbarProps> = ({ 
  activeTool, 
  onToolChange, 
  onToggleAIAssistant 
}) => {
  const { zoomIn, zoomOut, rotateClockwise, rotateCounterClockwise } = usePDF();

  // Tool definitions
  const tools = [
    { id: 'pointer', icon: 'cursor', label: 'Pointer' },
    { id: 'text', icon: 'type', label: 'Text' },
    { id: 'image', icon: 'image', label: 'Image' },
    { id: 'draw', icon: 'pen', label: 'Draw' },
    { id: 'highlight', icon: 'highlighter', label: 'Highlight' },
    { id: 'form', icon: 'layout', label: 'Form Fields' },
    { id: 'signature', icon: 'pen-tool', label: 'Signature' }
  ];

  return (
    <div className="toolbar">
      <div className="toolbar-group">
        <IconButton 
          icon="save" 
          label="Save" 
          onClick={() => console.log('Save document')} 
        />
        <IconButton 
          icon="printer" 
          label="Print" 
          onClick={() => console.log('Print document')} 
        />
        <IconButton 
          icon="download" 
          label="Download" 
          onClick={() => console.log('Download document')} 
        />
      </div>

      <div className="toolbar-group">
        {tools.map(tool => (
          <IconButton 
            key={tool.id}
            icon={tool.icon} 
            label={tool.label} 
            active={activeTool === tool.id}
            onClick={() => onToolChange(tool.id)} 
          />
        ))}
      </div>

      <div className="toolbar-group">
        <IconButton 
          icon="zoom-in" 
          label="Zoom In" 
          onClick={zoomIn} 
        />
        <IconButton 
          icon="zoom-out" 
          label="Zoom Out" 
          onClick={zoomOut} 
        />
        <IconButton 
          icon="rotate-cw" 
          label="Rotate Clockwise" 
          onClick={rotateClockwise} 
        />
        <IconButton 
          icon="rotate-ccw" 
          label="Rotate Counterclockwise" 
          onClick={rotateCounterClockwise} 
        />
      </div>

      <div className="toolbar-group">
        <IconButton 
          icon="cpu" 
          label="AI Assistant" 
          onClick={onToggleAIAssistant} 
        />
      </div>
    </div>
  );
};

export default Toolbar;
