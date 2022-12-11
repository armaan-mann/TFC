import React, {Component, useState, createContext, useEffect, useContext} from 'react';
import '../AllClasses/style.css';
import axios from "axios";
import { useNavigate } from "react-router-dom"
import {useParams, Link} from "react-router-dom";
import moment from 'moment';
import APIContext from "../../../Contexts/APIContext";

export default function AllClasses() {

    const navigate = useNavigate();
    // const { id } = useParams();
    const { user_id } = useParams();
    const { studio_id } = useParams();
    const { name } = useContext(APIContext);

    const [cid, setCid] = useState("");
    const [description, setDescription] = useState("");
    const [Name, setName] = useState("");
    const [Coach, setCoach] = useState("");
    const [Keywords, setKeywords] = useState("");
    const [capacity, setCapacity] = useState("");
    const [Studio, setStudio] = useState("")
    const [Start_Time, setStart_Time] = useState("");
    const [End_Time, setEnd_Time] = useState("");
    const [Start_Recursion, setStart_Recursion] = useState("");
    const [End_Recursion, setEnd_Recursion] = useState("");

    const [classAction, setClassAction] = useState("");
    const [option, setOption] = useState("");
    const [page, setPage] = useState(1);
    const [page_count, setPageCount] = useState(1);
    const [classList, setClassList] = useState([]);
    const [formErrors, setFormErrors] = useState("");

    const get_url = `http://127.0.0.1:8000/classes/${user_id}/${studio_id}/class/all/?page=${page}`;


    useEffect(() => {
        if (!localStorage.getItem('SavedToken')) {
            navigate('/login')
        }
        axios({
            method: "get",
            url: get_url,
            headers: {
                Authorization: localStorage.getItem('SavedToken')
            }
        })
            .then(res => {handle(res.data)
                setPageCount(res.data.page_count)
            })

    }, [page])

    function handle(res) {
        setCid(res.results[0]['id'])
        setDescription(res.results[0]["description"])
        setCapacity(res.results[0]["capacity"])
        setName(res.results[0]['name'])
        setCoach(res.results[0]['coach'])
        setKeywords(res.results[0]['keywords'])
        setStudio(res.results[0]['studio'])
        setStart_Time(res.results[0]['start_time'])
        setEnd_Time(res.results[0]['end_time'])
        setStart_Recursion(res.results[0]['start_recursion'])
        setEnd_Recursion(res.results[0]['end_recursion'])
    }


    return(
        <APIContext.Provider value={name}>
            <div className='all-div'>
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

                    <div className="user-logo">
                        <Link to={"/" + user_id + "/profile/"}>
                            <button className="user-btn">
                                <i className="fa-solid fa-user too"></i>
                            </button>
                        </Link>
                        <button id="icons" className="user-btn" onClick={() => {
                            localStorage.removeItem('SavedToken')
                            window.location.reload()
                        }
                        }>
                            <i id="icons" className="fa-solid fa-right-from-bracket too"></i>
                        </button>
                    </div>
                </header>
                <div className='main-title'>
                    <span class="blue">All Classes in {name}</span>
                </div>

                <table class="container">
                    <thead>
                    <tr className='col-heads'>

                        <th><span className='col'>Class ID</span></th>
                        <th><span className='col'>Name</span></th>
                        <th><span className='col'>Description</span></th>
                        <th><span className='col'>Studio</span></th>
                        <th><span className='col'>Coach</span></th>
                        <th><span className='col'>Keywords</span></th>
                        <th><span className='col'>Capacity</span></th>
                        <th><span className='col'>Start Time</span></th>
                        <th><span className='col'>End Time</span></th>
                        <th><span className='col'>Start Recursion</span></th>
                        <th><span className='col'>End Recursion</span></th>

                    </tr>
                    </thead>
                    <tbody className='last-hope'>
                    <tr>
                        <td className='roww'>{cid}</td>
                        <td className='roww'>{Name}</td>
                        <td className='roww'>{description}</td>
                        <td className='roww'>{Studio}</td>
                        <td className='roww'>{Coach}</td>
                        <td className='roww'>{Keywords}</td>
                        <td className='roww'>{capacity}</td>
                        <td className='roww'>{Start_Time}</td>
                        <td className='roww'>{End_Time}</td>
                        <td className='roww'>{Start_Recursion}</td>
                        <td className='roww'>{End_Recursion}</td>

                    </tr>
                    </tbody>
                </table>

                <div className='next-btn'>
                    { page > 1 ? <button className='bn' onClick={() =>   setPage(page - 1)}>Prev</button> : <></>}
                    { page < page_count ? <button className='bn' onClick={() =>   setPage(page + 1)}> Next </button>: <></>}
                </div>
                <Link to={"/" + user_id + "/class/" + cid + "/enrollment"}>
                    <button id="no" className='bn'>
                        Want to Enroll or Drop?
                    </button>
                </Link>
                <footer>
                    <h3>© Ansh, Armaan, Giancarlo </h3>
                </footer>
            </div>
        </APIContext.Provider>
    );
}



