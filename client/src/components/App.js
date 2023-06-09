import React, { useEffect, useState } from 'react';
import { Routes, Route, useParams} from 'react-router-dom';
import SideBar from './SideBar';
import Home from './Home';
import ForYou from './ForYou';
import Search from './Search';
import Settings from './Settings';
import Notifications from './Notifications';
import MessageCenter from './MessageCenter';

import ProfilePage from './ProfilePage';
import Create from './Create';

import Login from './Login';
import "./styles/SideBar.css"
import PostCard from './PostCard';






function App() {

  const param = useParams()
  const [user, setUser] = useState(null)
  const [refreshState, setRefrehState] = useState(false)

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
        <SideBar onLogout={setUser} user={user} />
        <Routes>
          <Route path='/' element={<Home setRefreshStage={setRefrehState} refreshState={refreshState} />} />
          <Route path='/foryou' element={<ForYou />} />
          <Route path="/profile/:userId" element={<ProfilePage setRefreshStage={setRefrehState} refreshState={refreshState} />} />
          <Route path='/posts/:postId' element={<PostCard setRefreshStage={setRefrehState} refreshState={refreshState} />} />
          <Route path='/create' element={<Create />} />
          <Route path='/search' element={<Search />} />
          <Route path='/settings' element={<Settings onAcctDelete={setUser} user={user} />} />
          <Route path='/notifications' element={<Notifications />} />
          <Route path='/messages' element={<MessageCenter />} />


        </Routes>
      </div>
    );
  }
};

export default App;