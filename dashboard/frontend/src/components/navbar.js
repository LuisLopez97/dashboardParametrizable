import React, { Component } from 'react';

class Navbar extends Component {
    render() {
        return <div className='bg-dark sticky-top'>
            <nav className="container navbar-expand-xl navbar-dark bg-dark text-center ">
                <a className="navbar-brand mt-4 mx-auto text-center" href="/">
                    <b>Navbar</b>
                </a>
                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse align-items-right" id="navbarSupportedContent">
                    <ul className="mr-5 pr-5 list-unstyled">
                        <li className="nav-item active my-5">
                            <a className="nav-link lead text-light text-center" href="/">
                                <span>
                                    <img src='static/home.svg' width="20" height="20" className="" alt=""></img>
                                </span>
                                Home
                                <span className="sr-only">(current)</span>
                                </a>
                        </li>
                        <li className="nav-item my-5">
                            <img src="static/table.svg" width="20" height="20" className="" alt=""></img>
                            <a className="nav-link lead text-light text-center" href="/">
                                Tweets
                            </a>
                        </li>
                        <li className="nav-item my-5">
                            <a className="nav-link lead text-light text-center" href="/">
                                <span>
                                    <img src="static/chart.svg" width="20" height="20" className="" alt=""></img>
                                </span>
                                Charts
                            </a>
                        </li>
                        <li className="nav-item my-5">
                            <a className="nav-link lead text-light text-center" href="/">
                                <span>
                                    <img src="static/map.svg" width="20" height="20" className="" alt=""></img>
                                </span>
                                Map
                            </a>
                        </li>
                    </ul>
                </div>
            </nav>
        </div>
    }
}

export default Navbar;