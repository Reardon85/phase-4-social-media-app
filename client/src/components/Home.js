import React from "react"
import "./styles/Home.css"

function Home() {

    return (
        <div class="card">
            <div class="card-image"></div>
            <div class="category"> Illustration </div>
            <div class="heading"> A heading that must span over two lines
                <div class="author"> By <span class="name">Abi</span> 4 days ago</div>
            </div>
        </div>
    )
}

export default Home