export interface TabConfig {
  id: string;
  label: string;
  component: React.ComponentType;
  icon?: string;
  disabled?: boolean;
}

export interface TabsProps {
  tabs: TabConfig[];
  defaultActiveTab?: number;
  onChange?: (activeIndex: number) => void;
}
