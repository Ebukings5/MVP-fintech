import React from 'react';
import './Features.css';

const Features = () => {
  return (
    <section className="features">
      <h2>Why Choose Us?</h2>
      <div className="feature">
        <h3>Track Expenses</h3>
        <p>Keep an eye on your spending with detailed expense tracking.</p>
      </div>
      <div className="feature">
        <h3>Manage Budgets</h3>
        <p>Set and manage budgets to stay on top of your finances.</p>
      </div>
      <div className="feature">
        <h3>Get Insights</h3>
        <p>Receive insightful reports and analytics to understand your spending habits.</p>
      </div>
    </section>
  );
};

export default Features;
