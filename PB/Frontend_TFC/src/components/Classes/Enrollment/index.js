import React, {Component, useState, createContext, useEffect, useContext} from 'react';
import '../Enrollment/style.css';
import axios from "axios";
import { useNavigate } from "react-router-dom"
import {useParams, Link} from "react-router-dom";
import moment from 'moment';
import APIContext from "../../../Contexts/APIContext";

// Reference: https://codepen.io/rickyeckhardt/pen/oNXeoZp

const Enrollment = () => {
    const navigate = useNavigate();
    const { user_id } = useParams();
    const { class_id } = useParams();
    const [className, setClassName] = useState("");
    const [option, setOp] = useState("");
    const [formErrors, setFormErrors] = useState("");
    const [listClasses, setListClasses] = useState([]);

    const send_url =  "http://127.0.0.1:8000/classes/" + user_id + "/" + "/class/" + class_id + "/enroll-drop/";

    useEffect(() => {
        axios({method: "get", url: "http://127.0.0.1:8000/classes/all/", headers: {
                Authorization: localStorage.getItem('SavedToken'),
            }}).then(res => { setListClasses(res.data)})
    })


    function Op(e) {
        console.log(e.target.value)
        setOp(e.target.value)
    }

    function Name(e){
        setClassName(e.target.value)
    }

    function handleEnrollment(res) {
        console.log(res)
        let k = Object.keys(res);
        if ('Success' in k) {
            alert("Enrolled!");
        }
    }

    function get_errors(keys, data){
        console.log(keys)
        console.log(data)
        let errors = {}
        for (let i = 0; i < keys.length; i++){
            console.log(keys)
            let k = keys[i]
            errors[k] = data.response.data[k]
        }

        setFormErrors(errors);
        console.log(errors)
        return errors
    }

    const enrollOrDrop = async(e) => {
        e.preventDefault();
        axios({
            method: "put",
            url: `http://localhost:8000/classes/${user_id}/class/${class_id}/enroll-drop/`,
            data: {
                _enrolled: className,
                _enroll_or_drop: option
            },
            headers: {
                Authorization: localStorage.getItem('SavedToken'),
            }
        }) .then(res => handleEnrollment(res))
            .catch(err => {
                    get_errors(Object.keys(err.response.data), err)
                }
            )
    };

    return (
            <div className='getPlan'>
                <header>
                    <div className="website-logo">
                        <img src="https://www.cs.toronto.edu/~kianoosh/courses/csc309/resources/images/tfc.png" alt="logo-tfc-picture"/>
                    </div>
                    <div className="navbar">
                        <nav>
                            <ul className="menuItems">
                                <li><a href='/main' data-item='Home'>Home</a></li>
                                <li><a href='/all' data-item='Classes'>Classes</a></li>
                                <li><a href='/studios' data-item='Studios'>Studios</a></li>
                                <li><a href='/plans' data-item='Subscriptions'>Subscriptions</a></li>
                            </ul>
                        </nav>
                    </div>
                </header>

                <div className="row-98">
                    <section className="section-2">
                        <main>
                            <div className="shadow-container">
                                <h1> Please choose your Enrollment Choice for the Class {class_id} </h1>

                                    <select id="status" value={className} onChange={e => Name(e)}>
                                        <option value="#">-----</option>
                                        {listClasses.map((c, index) => (
                                            <option key={index} value={c.name} onClick={event => setClassName(event.target.value)}>{c.name}</option>
                                        ))}
                                    </select>

                                <select id="status" value={option} onChange={event => Op(event)} required>
                                <option value="">-------</option>
                                <option value="enroll">Enroll </option>
                                <option value="drop">Drop</option>
                                <option value="enroll_all">Enroll All</option>
                                <option value="drop_all">Drop All</option>
                            </select>
                            <button id="boo" onClick={e => enrollOrDrop(e)}>
                                Finish
                            </button>
                                <span className="err-3"> {formErrors['Message']}</span>
                            </div>
                        </main>
                    </section>
                    <footer>
                        <h3>© Ansh, Armaan, Giancarlo </h3>
                    </footer>
                </div>
            </div>
    )
}

export default Enrollment;
