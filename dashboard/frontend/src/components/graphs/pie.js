import React, { Component } from 'react';
import { Pie } from 'react-chartjs-2';

export class Pies extends Component {
    render() {
        let positive = this.props.searchs.filter(({ Sentiment: c }) => c === 'positivo').length
        let negative = this.props.searchs.filter(({ Sentiment: c }) => c === 'negativo').length
        let neutral = this.props.searchs.filter(({ Sentiment: c }) => c === 'neutral').length

        const data = {
            labels: [
                'Positivo',
                'Negativo',
                'Neutro'
            ],
            datasets: [{
                data: [positive, negative, neutral],
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56'
                ],
                hoverBackgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56'
                ]
            }]
        };
        return (
            <div>
                <h2 className="d-none d-lg-block">Grafica de Pie</h2>
                <Pie data={data} />
            </div>
        )
    }
}

export default Pies
