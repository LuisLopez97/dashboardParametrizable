import React, { Component } from 'react'

export class wordClouds extends Component {
    render() {
        return (
            <div className="container">
                <div className="row p-4">
                    <div className="col-md-12 col-lg-6 card card-body px-3">
                        <img src="static/wordcloud_general.png" className="img-fluid" />
                    </div>
                    <div className="col-md-12 col-lg-6 card card-body px-3">
                        <img src="static/wordcloud_positivo.png" className="img-fluid" />
                    </div>
                </div>
                <div className="row p-4">
                    <div className="col-md-12 col-lg-6 card card-body px-3">
                        <img src="static/wordcloud_negativo.png" className="img-fluid" />
                    </div>
                    <div className="col-md-12 col-lg-6 card card-body px-3">
                        <img src="static/wordcloud_neutral.png" className="img-fluid" />
                    </div>
                </div>
            </div>
        )
    }
}

export default wordClouds
