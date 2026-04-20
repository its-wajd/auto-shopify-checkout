<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Shopify Checkout Workflow Automation</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      line-height: 1.7;
      max-width: 950px;
      margin: 0 auto;
      padding: 40px 20px;
      background: #0f1115;
      color: #e6e6e6;
    }
    h1, h2, h3 {
      color: #ffffff;
    }
    h1 {
      font-size: 2rem;
      border-bottom: 2px solid #2a2f3a;
      padding-bottom: 10px;
    }
    h2 {
      margin-top: 35px;
      color: #7cc7ff;
    }
    h3 {
      margin-top: 20px;
      color: #b8dfff;
    }
    p, li {
      color: #d6d6d6;
    }
    .badge {
      display: inline-block;
      padding: 6px 12px;
      margin: 6px 6px 6px 0;
      border-radius: 8px;
      background: #1b2230;
      color: #7cc7ff;
      font-size: 0.9rem;
    }
    .warning {
      background: #2a1a1a;
      border-left: 4px solid #ff5f5f;
      padding: 15px;
      border-radius: 8px;
      margin: 20px 0;
    }
    .info {
      background: #16202a;
      border-left: 4px solid #4db8ff;
      padding: 15px;
      border-radius: 8px;
      margin: 20px 0;
    }
    .section {
      margin-bottom: 28px;
    }
    ul {
      padding-left: 22px;
    }
    code {
      background: #1b2230;
      padding: 2px 6px;
      border-radius: 5px;
      color: #7cc7ff;
    }
    a {
      color: #7cc7ff;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
    .footer {
      margin-top: 40px;
      padding-top: 20px;
      border-top: 1px solid #2a2f3a;
      color: #9aa4b2;
    }
  </style>
</head>
<body>

  <h1>🧪 Shopify Checkout Workflow Automation</h1>
  <p><strong>Archived Security Research Project</strong></p>

  <div class="warning">
    <h2>⚠️ Disclaimer</h2>
    <p>
      This repository is published strictly for educational, research, and portfolio purposes.
    </p>
    <p>It explores how modern e-commerce platforms, specifically Shopify, handle:</p>
    <ul>
      <li>Session management</li>
      <li>Cookie persistence</li>
      <li>Token-based workflows</li>
      <li>Checkout state transitions</li>
    </ul>
    <p><strong>This project is NOT intended for real-world usage and must not be used for:</strong></p>
    <ul>
      <li>Unauthorized automation</li>
      <li>Payment system abuse</li>
      <li>Fraudulent activities</li>
    </ul>
    <p>
      Any misuse of this code is strictly prohibited. The author assumes no responsibility for improper use.
    </p>
  </div>

  <div class="section">
    <h2>📌 Project Status</h2>
    <p><strong>🚫 Archived / Non-Functional</strong></p>
    <p>This project is no longer operational due to:</p>
    <ul>
      <li>Platform security updates</li>
      <li>Anti-bot and anti-automation protections</li>
      <li>Changes in Shopify’s checkout infrastructure</li>
    </ul>
    <p>
      It is preserved as a technical research artifact and portfolio demonstration.
    </p>
  </div>

  <div class="section">
    <h2>🧠 Overview</h2>
    <p>
      This project is a workflow automation study of Shopify-based checkout systems.
    </p>
    <p>It was designed to analyze and replicate the technical flow of:</p>
    <ul>
      <li>Storefront navigation</li>
      <li>Product and variant discovery</li>
      <li>Cart interaction</li>
      <li>Checkout session initialization</li>
      <li>Token extraction and request replication</li>
      <li>GraphQL-based checkout communication</li>
    </ul>
    <p>
      The goal is to understand how complex web systems manage state, security, and transaction flow.
    </p>
  </div>

  <div class="section">
    <h2>🏗️ Architecture</h2>
    <p>
      The codebase (~2200 lines) is structured in a clean, modular, class-based design, with a focus on readability and maintainability.
    </p>

    <h3>🔹 Core Components</h3>

    <div class="info">
      <h3>Storage</h3>
      <ul>
        <li>Persistent storage layer (JSON-based)</li>
        <li>Manages cookies, tokens, and site-specific data</li>
        <li>Supports session continuity across requests</li>
        <li>Includes structured address generation with API fallback logic</li>
      </ul>
    </div>

    <div class="info">
      <h3>Checker</h3>
      <ul>
        <li>Main automation engine</li>
        <li>Handles storefront navigation and product discovery</li>
        <li>Extracts collections, products, and variants</li>
        <li>Manages cart and checkout initialization</li>
        <li>Parses tokens from responses and redirects</li>
      </ul>
    </div>

    <div class="info">
      <h3>Session</h3>
      <ul>
        <li>Handles checkout session lifecycle</li>
        <li>Builds and submits structured requests</li>
        <li>Simulates multi-step checkout interactions</li>
        <li>Manages final transaction flow logic</li>
      </ul>
    </div>

    <div class="info">
      <h3>Utilities</h3>
      <ul>
        <li>Proxy handling and session configuration</li>
        <li>Randomized data generation</li>
        <li>HTML parsing and extraction</li>
        <li>Request orchestration helpers</li>
      </ul>
    </div>
  </div>

  <div class="section">
    <h2>🔍 Technical Concepts Demonstrated</h2>
    <ul>
      <li>Advanced HTTP request replication</li>
      <li>Stateful session and cookie management</li>
      <li>Token extraction from HTML content</li>
      <li>Token extraction from meta tags</li>
      <li>Token extraction from redirect chains</li>
      <li>Shopify GraphQL request construction</li>
      <li>Dynamic header and payload generation</li>
      <li>Multi-step workflow automation</li>
      <li>Handling real-world web application constraints</li>
    </ul>
  </div>

  <div class="section">
    <h2>🎯 Learning Objectives</h2>
    <p>This project demonstrates:</p>
    <ul>
      <li>How modern checkout systems operate internally</li>
      <li>How platforms implement anti-automation protections</li>
      <li>How to structure large-scale Python automation projects</li>
      <li>How session-based workflows are maintained across requests</li>
    </ul>
  </div>

  <div class="section">
    <h2>⚖️ Ethical Use</h2>
    <p>This project should only be used for:</p>
    <ul>
      <li>Security research</li>
      <li>Educational analysis</li>
      <li>Authorized testing environments</li>
    </ul>
    <p>If you are interested in this domain, focus on:</p>
    <ul>
      <li>Bug bounty programs</li>
      <li>Responsible disclosure</li>
      <li>Ethical penetration testing</li>
    </ul>
    <p>
      Never interact with systems without proper authorization.
    </p>
  </div>

  <div class="section">
    <h2>📁 Notes</h2>
    <ul>
      <li>Code is provided as-is</li>
      <li>No updates or support will be provided</li>
      <li>Some parts may be intentionally outdated or incomplete</li>
    </ul>
  </div>

  <div class="section">
    <h2>👨‍💻 Author</h2>
    <p><strong>Wajd Dev</strong></p>
    <p>
      GitHub:
      <a href="https://github.com/its-wajd" target="_blank">https://github.com/its-wajd</a>
    </p>
    <p>Focused on:</p>
    <span class="badge">Python Development</span>
    <span class="badge">Web Scraping &amp; Automation</span>
    <span class="badge">Security Research</span>
    <span class="badge">Reverse Engineering</span>
  </div>

  <div class="footer">
    <p>© Wajd Dev — Research Archive</p>
  </div>

</body>
</html>
