import React, { Component } from 'react';

class Navbar extends Component {
    render() {
        return (
            <nav className="navbar navbar-expand-lg flex-lg-column text-center">
                <a className="h5 py-lg-5 text-white" href="#">Navbar</a>
                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarColor01" aria-controls="navbarColor01" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse" id="navbarColor01">
                    <div className="navbar-nav flex-column">
                        <a className="nav-item nav-link py-3" href="#">Home</a>
                        <a className="nav-item nav-link py-3" href="/#/Tweets">Tweets</a>
                        <a className="nav-item nav-link py-3" href="/#/Charts">Charts</a>
                        <a className="nav-item nav-link py-3" href="/#/WordClouds">Clouds</a>
                    </div>
                </div>
            </nav>
        )
    }
}

export default Navbar;