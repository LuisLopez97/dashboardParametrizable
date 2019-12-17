import React, { Component } from 'react';
import { Widget, addResponseMessage, setQuickButtons } from 'react-chat-widget';


import './css/styles.css'


class ChatBot extends Component {

    componentDidMount() {
        addResponseMessage("Bienvenido  al chatbot de la Secretaría de Economía! ¿Necesita alguna ayuda con la convocatoria?",
            setQuickButtons
                ([{ label: '¿Convocatorias disponibles en la UDP?', value: 0 },
                { label: '¿Quienes pueden participar?', value: 1 },
                { label: '¿Requisitos para participar?', value: 2 },
                { label: '¿Tipos de apoyo que se pueden solicitar?', value: 3 },
                { label: 'Montos de apoyo', value: 4 }]));
    }


    //al apretar el boton dice lo de value
    handleQuickButtonClicked = (respuesta) => {

        if (respuesta == 0) {
            addResponseMessage("Estudiante, 9no, 8.5");
        }
        else if (respuesta == 1) {
            addResponseMessage("Curp, INE, RFC",
                setQuickButtons
                    ([{
                        label: '    Buscar curp    ', value: 'https://www.gob.mx/curp/',
                        target: '_blank'
                    }]));
        }
        else if (respuesta == 2) {
            setQuickButtons([{ label: 'Monto', value: '$44,000' },
            { label: 'Vigencia', value: 'Año 2020' },
            { label: 'Cobertura', value: 'México y Canadá' }]);

        }
        else {
            addResponseMessage(respuesta)
        }
    }
    handleNewUserMessage = (newMessage) => {
        console.log(`New message incoming! ${newMessage}`);
        // Now send the message throught the backend API
        if (newMessage === 'requisitos') {
            addResponseMessage("Estudiante, 9no, 8.5");
        }
        else if (newMessage === 'registro') {
            addResponseMessage("Curp, INE, RFC",
                setQuickButtons
                    ([{
                        label: '    Buscar curp    ', value: 'https://www.gob.mx/curp/', link: 'https://www.gob.mx/curp/'
                    }]));
        }
        else if (newMessage === 'generales') {
            setQuickButtons([{ label: 'Monto', value: '$44,000' },
            { label: 'Vigencia', value: 'Año 2020' },
            { label: 'Cobertura', value: 'México y Canadá' }]);
        }

    }



    render() {
        return (
            <div className="App">

                <header className="App-header">
                    <h1 className="App-tittle">Chatbot</h1>
                </header>
                <div>


                    <Widget
                        handleNewUserMessage={this.handleNewUserMessage}
                        title="Secretaría de Economía"
                        subtitle="Chatbot de la Secretaría de Economía"
                        handleQuickButtonClicked={this.handleQuickButtonClicked}
                        senderPlaceHolder="Escribe tu mensaje..."



                    />





                </div>
            </div>
        );

    }

}


export default ChatBot;