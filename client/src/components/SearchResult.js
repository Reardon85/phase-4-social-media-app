import React from 'react'
import "./styles/SearchResult.css"
import SearchCard from './SearchCard';



function SearchResult({ filteredUsers, handleClick }) {


    const user_array = filteredUsers.length > 0 ? filteredUsers.map((user) => {

        return <SearchCard key={user.id} {...user} handleClick={handleClick} />
    }) : <></>

    return (
        <div>
            <div className="result-card">
                {user_array}
            </div>
        </div>
    );
}


export default SearchResult