import Tabs from "./components/Tabs";
import Home from "./pages/Home";
import Settings from "./pages/Settings";
import { TabConfig } from "./types";
import "./App.css";

function App() {
  const tabs: TabConfig[] = [
    {
      id: "home",
      label: "Home",
      component: Home,
      icon: "🏠",
    },
    {
      id: "settings",
      label: "Settings",
      component: Settings,
      icon: "⚙️",
    },
  ];

  const handleTabChange = (activeIndex: number) => {
    console.log("Active tab changed to:", activeIndex);
    // You can perform additional actions here
    // e.g., update URL, track analytics, etc.
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Multi-Page Tabs Application</h1>
        <p className="subtitle">Built with React & TypeScript</p>
      </header>

      <main>
        <Tabs tabs={tabs} defaultActiveTab={0} onChange={handleTabChange} />
      </main>

      <footer className="app-footer">
        <p>&copy; 2024 Your Company. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
