import React from "react";

interface StatCardProps {
  title: string;
  value: string | number;
}

const StatCard: React.FC<StatCardProps> = ({ title, value }) => (
  <div className="stat-card">
    <h3>{title}</h3>
    <p>{value}</p>
  </div>
);

const Home: React.FC = () => {
  return (
    <div className="page home-page">
      <h2>🏠 Home Page</h2>
      <p>Welcome to the home page! This is your dashboard.</p>

      <div className="stats">
        <StatCard title="Users" value="1,234" />
        <StatCard title="Revenue" value="$45,678" />
        <StatCard title="Active Sessions" value="89" />
      </div>

      <div className="recent-activity">
        <h3>Recent Activity</h3>
        <ul>
          <li>New user registered: John Doe</li>
          <li>Payment received: $1,200</li>
          <li>Server updated to v2.1.0</li>
        </ul>
      </div>
    </div>
  );
};

export default Home;
