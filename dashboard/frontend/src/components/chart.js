import React, { Component } from 'react';
import { Bar } from 'react-chartjs-2';


class Chart extends Component {
    // constructor (props){
    //     super(props);
    // }
    getCount = function () {
        var data = this.props.data;
        var neutro = data.filter(function (d) { return d.sentiment === "neutral"; }).length,
            positivo = data.filter(function (d) { return d.sentiment === "positive"; }).length,
            negativo = data.filter(function (d) { return d.sentiment === "negative"; }).length;
        var cantidadDatos = [neutro, positivo, negativo, 0];
        return cantidadDatos;
    }
    render() {
        var startingData = {
            labels: ['Neutro', 'Positivo', 'Negativo'],
            datasets: [
                {
                    label: "Sentimientos",
                    backgroundColor: 'green,white',
                    borderColor: 'black',
                    borderWidth: 2,
                    data: this.getCount()
                }
            ]
        }
        return (
            <div className="card bg-light">
                <h1 className="display-4 text-center">
                    Distribución de Sentimientos
                </h1>
                <Bar
                    data={startingData}
                    options={{
                        title: {
                            display: true,
                            text: '',
                            fontSize: 20
                        },
                        legend: {
                            display: true,
                            position: 'center'
                        }
                    }}
                />
                <div className="card-body text-center">
                    <h5 className="card-title">
                        Grafica Previa
                    </h5>
                    <p className="card-text">
                        Una vista previa a la distribución de sentimientos.
                    </p>
                    <a href="/" className="btn btn-warning">Ir a Graficas</a>
                </div>
            </div>
            // <div>
            //     <XYPlot height={300} width={300}>
            //         <LineSeries data={data} />
            //     </XYPlot>
            // </div>
        )
    }
}

export default Chart;