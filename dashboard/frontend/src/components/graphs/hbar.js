import React, { Component } from 'react'
import { HorizontalBar } from 'react-chartjs-2'

export class Hbar extends Component {
    render() {
        let positive = this.props.searchs.filter(({ Sentiment: c }) => c === 'positivo').length
        let negative = this.props.searchs.filter(({ Sentiment: c }) => c === 'negativo').length
        let neutral = this.props.searchs.filter(({ Sentiment: c }) => c === 'neutral').length

        const data = {
            labels: [
                'Positivo', 'Negativo', 'Neutral',
            ], datasets: [
                {
                    label: 'Sentimientos',
                    backgroundColor: 'rgba(255,99,132,0.2)',
                    borderColor: 'rgba(255,99,132,1)',
                    borderWidth: 1,
                    hoverBackgroundColor: 'rgba(255,99,132,0.4)',
                    hoverBorderColor: 'rgba(255,99,132,1)',
                    data: [positive, negative, neutral, 0]
                }
            ]
        };
        return (
            <div>
                <h2 className="d-none d-lg-block">Barra Horizontal</h2>
                <HorizontalBar data={data} />
            </div>
        )
    }
}

export default Hbar
