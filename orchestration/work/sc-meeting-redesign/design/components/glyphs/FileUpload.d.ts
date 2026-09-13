import * as React from 'react';
export interface FileUploadProps {
  className?: string;
  style?: React.CSSProperties;
  file?: boolean;
  state?: "normal" | "dropdown";
  /** Text content; defaults to "첨부할 파일을 끌어다 놓거나 추가하세요". */
  text1?: string;
}
export declare const FileUpload: React.FC<FileUploadProps>;
export default FileUpload;
