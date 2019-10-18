import React, { Componet, Fragment } from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import store from '../store';
import { HashRouter as Router, Route, Switch, Redirect } from 'react-router-dom';


// Componentes
import Navbar from './navbar'
import Section1 from './section1'

class App extends React.Component {

    render() {
        return (
            <Provider store={store}>
                <Fragment >
                    <div className="bg-primary">
                        <div className="container-fluid">
                            <div className="row bg-primary">
                                <div className="col-xl-1 lg-1 md-1 sm-1 sticky-top bg-primary">
                                    <Navbar />
                                </div>
                                <div className="col-xl-11 lg-10 md-10 sm-11 bg-light">
                                    <Router>
                                        <Switch>
                                            <Route exact path="/"
                                                component={Section1} />
                                        </Switch>
                                    </Router>
                                </div>
                            </div>
                        </div>
                    </div>
                </Fragment>
            </Provider>
        )
    }
}

ReactDOM.render(<App />, document.getElementById('app'));