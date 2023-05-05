import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from './Home';
import SideBar from './SideBar';
function App() {

  return (
    <div className="App">
      <SideBar />
      <Routes>
        <Route path='/' element={<Home />} />

      </Routes>
    </div>
  );
};

export default App;