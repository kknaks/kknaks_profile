import * as React from 'react';
export interface PageHeaderProps {
  className?: string;
  style?: React.CSSProperties;
  slotsContainer?: string;
  pageTitle?: string;
  breadcrumb?: boolean;
  /** Text content; defaults to "페이지 제목". */
  text1?: string;
}
export declare const PageHeader: React.FC<PageHeaderProps>;
export default PageHeader;
