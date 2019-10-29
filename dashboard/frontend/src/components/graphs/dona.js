import React, { Component } from 'react'
import { Doughnut } from 'react-chartjs-2'

export class Dona extends Component {
    render() {
        let cant = this.props.searchs.filter(({ negativereason: c }) => c === "Can't Tell").length
        let customer = this.props.searchs.filter(({ negativereason: c }) => c === 'Customer Service Issue').length
        let late = this.props.searchs.filter(({ negativereason: c }) => c === 'Late Flight').length
        let cancelled = this.props.searchs.filter(({ negativereason: c }) => c === 'Cancelled Flight').length
        let lost = this.props.searchs.filter(({ negativereason: c }) => c === 'Lost Luggage').length

        const data = {
            labels: [
                'No se sabe',
                'Mala atención al cliente',
                'Vuelo atrasado',
                'Vuelo cancelado',
                'Perdida de equipaje'
            ],
            datasets: [{
                data: [cant, customer, late, cancelled, lost],
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    'rgba(48,186,95,0.5)',
                    'rgba(112,48,186,0.5)',
                ],
                hoverBackgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    'rgba(48,186,95,1)',
                    'rgba(112,48,186,1)',
                ]
            }]
        };
        return (
            <div>
                <h2 className="d-none d-lg-block">Grafica de Dona</h2>
                <Doughnut data={data} />
            </div>
        )
    }
}

export default Dona
