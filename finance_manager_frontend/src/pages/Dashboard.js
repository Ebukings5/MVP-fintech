import React, { useState } from 'react';
import Login from '../components/Login';
import SignUp from '../components/SignUp';

const Dashboard = () => {
  const [showLogin, setShowLogin] = useState(true);

  return (
    <div>
      <h1>Welcome to the Finance Manager Dashboard</h1>
      <div>
        <button onClick={() => setShowLogin(true)}>Login</button>
        <button onClick={() => setShowLogin(false)}>Sign Up</button>
      </div>
      <div>
        {showLogin ? <Login /> : <SignUp />}
      </div>
    </div>
  );
};

export default Dashboard;
