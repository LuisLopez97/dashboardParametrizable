import React, { Component } from 'react'

export class Pagination extends Component {
    constructor(props) {
        super(props);
    }
    disablePrev = () => {
        if (this.props.currentPage == 1) {
            document.getElementById("previous").className = "page-item disabled"
        }
    }

    render() {
        return (
            <nav aria-label="Page navigation example">
                <ul className="pagination">
                    <li className="page-item"><a className="btn page-link disabled border" id="previous">Previous</a></li>
                    <li className="page-item active"><a className="btn page-link border">{this.props.currentPage}</a></li>
                    <li className="page-item"><a className="btn page-link border">{this.props.currentPage + 1}</a></li>
                    <li className="page-item"><a className="btn page-link border">{this.props.currentPage + 2}</a></li>
                    <li className="page-item"><a className="btn page-link border">{this.props.currentPage + 3}</a></li>
                    <li className="page-item"><a className="btn page-link border">{this.props.currentPage + 4}</a></li>
                    <li className="page-item"><a className="btn page-link disabled border" id="Next">Next</a></li>
                </ul>
            </nav>
        )
    }
}

export default Pagination
