import React, { useState } from "react";
import { TabsProps } from "../types";
import "./Tabs.css";

const Tabs: React.FC<TabsProps> = ({
  tabs,
  defaultActiveTab = 0,
  onChange,
}) => {
  const [activeTab, setActiveTab] = useState<number>(defaultActiveTab);

  const handleTabClick = (index: number) => {
    setActiveTab(index);
    onChange?.(index);
  };

  const ActiveComponent = tabs[activeTab].component;

  return (
    <div className="tabs-container">
      {/* Tab Headers */}
      <div className="tab-headers" role="tablist">
        {tabs.map((tab, index) => (
          <button
            key={tab.id}
            role="tab"
            aria-selected={activeTab === index}
            aria-controls={`tabpanel-${tab.id}`}
            id={`tab-${tab.id}`}
            className={`tab-btn ${activeTab === index ? "active" : ""} ${tab.disabled ? "disabled" : ""}`}
            onClick={() => !tab.disabled && handleTabClick(index)}
            disabled={tab.disabled}
          >
            {tab.icon && <span className="tab-icon">{tab.icon}</span>}
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div
        className="tab-content-wrapper"
        role="tabpanel"
        id={`tabpanel-${tabs[activeTab].id}`}
        aria-labelledby={`tab-${tabs[activeTab].id}`}
      >
        <ActiveComponent />
      </div>
    </div>
  );
};

export default Tabs;
