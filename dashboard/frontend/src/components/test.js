import React, { Component } from 'react'

export class Test extends Component {
    render() {
        return (
            <div>
                <h1>Hola prueba</h1>
                <form action="/test" method="POST">
                    <button type="submit" value="Submit" className="btn btn-info">Enviar</button>
                </form>
            </div>
        )
    }
}

export default Test
