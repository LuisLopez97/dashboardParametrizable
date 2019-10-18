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
    render() {
        return (
            <div className="">
                AQUI IRA UNA NAVBAR CUANDO ESTE LISTAAA
                <hr />
                <div className="navbar navbar-dark">
                    <ul className="navbar-nav">
                        <li className="nav-item">
                            <a href="/" className="nav-link">LINK</a>
                        </li>
                        <li className="nav-item">
                            <a href="/" className="nav-link">LINK</a>
                        </li>
                        <li className="nav-item">
                            <a href="/" className="nav-link">LINK</a>
                        </li>
                    </ul>
                </div>
            </div>
        )
    }
}

export default Navbar;