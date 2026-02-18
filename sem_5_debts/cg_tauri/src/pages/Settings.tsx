import React, { useState } from "react";

interface UserSettings {
  notifications: boolean;
  darkMode: boolean;
  emailFrequency: "daily" | "weekly" | "monthly" | "never";
  language: string;
}

const Settings: React.FC = () => {
  const [settings, setSettings] = useState<UserSettings>({
    notifications: true,
    darkMode: false,
    emailFrequency: "weekly",
    language: "en",
  });

  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [saveMessage, setSaveMessage] = useState<string | null>(null);

  const handleToggle = (
    key: keyof Pick<UserSettings, "notifications" | "darkMode">,
  ) => {
    setSettings((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const { name, value } = e.target;
    setSettings((prev) => ({ ...prev, [name]: value }));
  };

  const handleSave = async () => {
    setIsSaving(true);
    setSaveMessage(null);

    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1000));
      setSaveMessage("Settings saved successfully!");
    } catch (error) {
      setSaveMessage("Failed to save settings. Please try again.");
    } finally {
      setIsSaving(false);
      setTimeout(() => setSaveMessage(null), 3000);
    }
  };

  const handleReset = () => {
    if (window.confirm("Are you sure you want to reset all settings?")) {
      setSettings({
        notifications: true,
        darkMode: false,
        emailFrequency: "weekly",
        language: "en",
      });
    }
  };

  return (
    <div className="page settings-page">
      <h2>⚙️ Settings</h2>

      {saveMessage && (
        <div
          className={`alert ${saveMessage.includes("Failed") ? "error" : "success"}`}
        >
          {saveMessage}
        </div>
      )}

      <div className="settings-section">
        <h3>Preferences</h3>

        <div className="setting-item">
          <label className="toggle-label">
            <span>Enable notifications</span>
            <input
              type="checkbox"
              checked={settings.notifications}
              onChange={() => handleToggle("notifications")}
              disabled={isSaving}
            />
            <span className="toggle-slider"></span>
          </label>
        </div>

        <div className="setting-item">
          <label className="toggle-label">
            <span>Dark mode</span>
            <input
              type="checkbox"
              checked={settings.darkMode}
              onChange={() => handleToggle("darkMode")}
              disabled={isSaving}
            />
            <span className="toggle-slider"></span>
          </label>
        </div>

        <div className="setting-item">
          <label htmlFor="emailFrequency">Email frequency:</label>
          <select
            id="emailFrequency"
            name="emailFrequency"
            value={settings.emailFrequency}
            onChange={handleChange}
            disabled={isSaving}
          >
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
            <option value="never">Never</option>
          </select>
        </div>

        <div className="setting-item">
          <label htmlFor="language">Language:</label>
          <select
            id="language"
            name="language"
            value={settings.language}
            onChange={handleChange}
            disabled={isSaving}
          >
            <option value="en">English</option>
            <option value="es">Español</option>
            <option value="fr">Français</option>
            <option value="de">Deutsch</option>
          </select>
        </div>
      </div>

      <div className="settings-section">
        <h3>Account</h3>

        <div className="button-group">
          <button
            onClick={handleSave}
            disabled={isSaving}
            className="btn-primary"
          >
            {isSaving ? "Saving..." : "Save Settings"}
          </button>

          <button
            onClick={handleReset}
            disabled={isSaving}
            className="btn-secondary"
          >
            Reset to Default
          </button>

          <button className="btn-danger" disabled={isSaving}>
            Delete Account
          </button>
        </div>
      </div>
    </div>
  );
};

export default Settings;
