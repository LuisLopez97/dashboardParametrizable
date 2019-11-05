import React, { Component } from 'react'
import { HorizontalBar } from 'react-chartjs-2'

export class Hbar extends Component {
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
            ], datasets: [
                {
                    label: 'Sentimientos',
                    backgroundColor: 'rgba(255,99,132,0.2)',
                    borderColor: 'rgba(255,99,132,1)',
                    borderWidth: 1,
                    hoverBackgroundColor: 'rgba(255,99,132,0.4)',
                    hoverBorderColor: 'rgba(255,99,132,1)',
                    data: [cant, customer, late, cancelled, lost]
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
