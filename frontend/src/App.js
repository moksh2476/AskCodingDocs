import React from "react";
import UrlConverter from "./components/UrlConverter";
import DocChat from "./components/DocChat";
import "./App.css"; // Import the CSS file

export default function App() {
  return (
    <div className="app-container">
      <h1 className="app-title">🧠 Generative AI Documentation Assistant</h1>

      <div className="columns">
        <div className="column">
          <UrlConverter />
        </div>
        <div className="column">
          <DocChat />
        </div>
      </div>
    </div>
  );
}
