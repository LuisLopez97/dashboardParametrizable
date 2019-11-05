import React, { Component } from 'react';
import { Bar } from 'react-chartjs-2';


export class Bars extends Component {

    render() {
        let positive = this.props.searchs.filter(({ airline_sentiment: c }) => c === 'positive').length
        let negative = this.props.searchs.filter(({ airline_sentiment: c }) => c === 'negative').length
        let neutral = this.props.searchs.filter(({ airline_sentiment: c }) => c === 'neutral').length

        const data = {
            labels: ['Positivo', 'Negativo', 'Neutral'],
            datasets: [
                {
                    label: 'Cantidad',
                    backgroundColor: 'rgba(205,71,90,0.5)',
                    borderWidth: 1,
                    hoverBorderColor: 'rgba(11,11,11,1)',
                    data: [positive, negative, neutral, 0]
                }
            ]
        };
        return (
            <div>
                <h2 className="d-none d-lg-block">Grafica de Barras</h2>
                <Bar
                    data={data}
                    width={100}
                    height={50}
                />
            </div>
        )
    }
}

export default Bars
