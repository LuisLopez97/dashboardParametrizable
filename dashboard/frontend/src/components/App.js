import React, { Componet, Fragment } from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import store from '../store';
import { HashRouter as Router, Route, Switch, Redirect } from 'react-router-dom';


// Componentes
import Navbar from './navbar'
import Section1 from './section1'
import DataTable from './dataTable';
import Chart from './chart';

class App extends React.Component {

    render() {
        return (
            <Provider store={store}>
                <Fragment >
                    <div className="bg-primary">
                        <div className="container-fluid">
                            <div className="row bg-primary">
                                <div className="col-lg-1 navbar-dark bg-primary sidebar sidebar-sticky">
                                    <Navbar />
                                </div>
                                <div className="col-lg-11 bg-secondary">
                                    <Router>
                                        <Switch>
                                            <Route exact path="/"
                                                component={Section1} />
                                            <Route exact path="/Tweets"
                                                component={DataTable} />
                                            <Route exact path="/Charts"
                                                component={Chart} />
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