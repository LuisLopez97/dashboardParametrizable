import React, { Component } from 'react';

{/* <div className='bg-primary sticky-top'>
            <nav className="container navbar-expand-xl navbar-dark bg-primary text-center ">
                <a className="navbar-brand mt-4 mx-auto text-center" href="/">
                    <b>Navbar</b>
                </a>
                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse align-items-right" id="navbarSupportedContent">
                    <ul className="mr-auto pr-auto list-unstyled">
                        <li className="nav-item my-5">
                            <a className="nav-link active lead text-light text-center" href="/">
                                <span>
                                    <img src='static/home.svg' width="20" height="20" className="" alt=""></img>
                                </span>
                                Home
                                <span className="sr-only">(current)</span>
                            </a>
                        </li>
                        <li className="nav-item my-5">
                            <img src="static/table.svg" width="20" height="20" className="d-inline" alt=""></img>
                            <a className="nav-link lead text-light text-center d-inline" href="/">
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
                                    <img src="static/map.svg" width="20" height="20" className="d-block mx-4" alt=""></img>
                                </span>
                                Map
                            </a>
                        </li>
                    </ul>
                </div>
            </nav>
        </div> */}


class Navbar extends Component {
    constructor(props) {
        super(props);
    }
    getDate = () => {
        console.log("holamundo")
    }
    render() {
        return (
            <nav>
                <div className="mt-5">
                    <a className="h3 text-light mt-5 pt-5" href="/">Navbar</a>
                </div>
                <div className="mt-3 text-center text-light navbar-dark bg-primary my-5">
                    <ul className="navbar-nav text-center">
                        <li className="nav-item mt-3 py-5 d-none d-md-block">
                            <a className="nav-link" href="#">Home</a>
                        </li>
                        <li className="nav-item mt-3 py-5 d-none d-md-block">
                            <a className="nav-link" href="/#/Tweets">Tweets</a>
                        </li>
                        <li className="nav-item mt-3 py-5 d-none d-md-block">
                            <a className="nav-link" href="#">Chart</a>
                        </li>
                    </ul>
                </div>
                <footer>
                    <p className="text-light h-6" id="fecha">
                    </p>
                </footer>
            </nav>
        )
    }
}

export default Navbar;