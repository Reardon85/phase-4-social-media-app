import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useFormik } from "formik";

import { Button, Form, Grid, Header, Message, Segment } from 'semantic-ui-react'
import * as yup from "yup";
import Register from "./Register";

// import "./styles/Login.css"

function Login({ onLogin }) {

    const [refreshPage, setRefreshPage] = useState(false)
    const [errors, setErrors] = useState([])
    const [register, setRegister] = useState(false)
    const navigate = useNavigate()

    useEffect(() => {



    }, [refreshPage])


    // const formSchema = yup.object()
    const formSchema = yup.object().shape({
        username: yup.string().required("Must enter a name").max(15),
        password: yup.string().required("Must enter a name").max(15),

    });

    const formik = useFormik({
        initialValues: {
            username: "",
            password: "",
        },
        validationSchema: formSchema,
        onSubmit: (values) => {
            console.log("submit is working")
            // might want to seterrors to [] here fdf
            fetch('/login', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(values, null, 2),
            })
                .then((res) => {
                    if (res.ok) {
                        //might want to set refresh page here
                        res.json().then((user) => {
                            onLogin(user)
                        })
                    }
                    else {
                        res.json().then((err) => setErrors(err.error))
                    }
                });
        },
    });

    return (
        register ?
            <div className="login">
                <Register onLogin={onLogin} setRegister={setRegister} />
            </div>
            :
            <div className="login">
                <Grid textAlign='center' style={{ height: '100vh' }} verticalAlign='middle'>
                    <Grid.Column style={{ maxWidth: 850, margin: 'auto' }}>
                        <Form size='large' onSubmit={formik.handleSubmit}>
                            <Header as='h2' color='black' textAlign='center'>
                                {/* <Image src={logo}  /> */} Log In
                            </Header>
                            <Segment stacked>
                                <Form.Input
                                    fluid icon='user'
                                    iconPosition='left'
                                    id="username"
                                    name="username"
                                    placeholder='Username'
                                    onChange={formik.handleChange}
                                    value={formik.values.username}
                                />
                                <Form.Input
                                    fluid
                                    icon='lock'
                                    iconPosition='left'
                                    id='password'
                                    type='password'
                                    name="password"
                                    placeholder='Password'
                                    onChange={formik.handleChange}
                                    value={formik.values.password}
                                />
                                <Button className="login-btn" color='black' fluid size='large' type='submit'>
                                    Login
                                </Button>
                            </Segment>
                            <Message className="message" >
                                New to us? <Button className="login-btn1" onClick={() => setRegister(true)}>Sign Up</Button>
                            </Message>
                        </Form>
                    </Grid.Column>
                </Grid>

            </div >
    )
}

export default Login
