import React, { Componet } from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import store from '../store';
import { HashRouter as Router, Route, Switch } from 'react-router-dom';


// Componentes
import Navbar from './navbar'
import Section1 from './section1'
import DataTable from './dataTable';
import Chart from './chart';
import WordClouds from './wordClouds';

class App extends React.Component {

    render() {
        return (
            <Provider store={store}>
                <div className="bg-primary container-fluid">
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
                                    <Route exact path="/WordClouds"
                                        component={WordClouds} />
                                </Switch>
                            </Router>
                        </div>
                    </div>
                </div>
            </Provider>
        )
    }
}

ReactDOM.render(<App />, document.getElementById('app'));