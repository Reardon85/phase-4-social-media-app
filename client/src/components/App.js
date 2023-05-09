import React, { useEffect, useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import SideBar from './SideBar';
import Home from './Home';
import ForYou from './ForYou';
import Search from './Search';

import ProfilePage from './ProfilePage';

import Login from './Login';
import "./styles/SideBar.css"






function App() {

  const [user, setUser] = useState(null)

  useEffect(() => {
    //auto-login
    fetch('/check_session')
      .then((r) => {
        if (r.ok) {
          r.json().then((user) => setUser(user))
        } else {
          setUser("none")
        }
      })
  }, [])


  if (user === "none") {
    return <Login onLogin={setUser} user={user} />
  } else if (user) {
    return (
      <div className="App">
        <SideBar onLogout={setUser} user={user}  />
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/foryou' element={<ForYou />} />
          <Route path= "/profile/:userId" element={<ProfilePage />} />
          <Route path='/search' element={<Search />} />
           
        </Routes>
      </div>
    );
  }
};

export default App;