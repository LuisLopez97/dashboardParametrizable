import React, { Componnet } from 'react';
import ReactDOM from 'react-dom';

// Componentes
import Navbar from './navbar'
import Section1 from './section1'

// Json
import data from './sample/tweetsp.json';

class App extends React.Component{
    state = {
        data:data
    }
    render(){
        return (
            <div className="bg-primary">
                <div className="container-fluid">
                    <div className="row bg-dark">
                        <div className="col-xl-1 lg-2 md-2 sm-1 sticky-top bg-dark">
                            <Navbar />
                        </div>
                        <div className="col-xl-11 lg-10 md-10 sm-11 bg-light">
                            <Section1 data={this.state.data} />
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

ReactDOM.render(<App />, document.getElementById('app'));