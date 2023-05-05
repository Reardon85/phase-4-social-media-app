import React from 'react';
import { Routes, Route } from 'react-router-dom';
import SideBar from './SideBar';
import Home from './Home';
import ForYou from './ForYou';


function App() {

  return (
    <div className="App">
      <SideBar />
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/foryou' element={<ForYou />} />
      </Routes>
    </div>
  );
};

export default App;