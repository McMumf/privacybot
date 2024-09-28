import React, { useEffect } from 'react';
import {
    Routes,
    Route,
    useLocation
} from 'react-router-dom';

import './css/style.scss';

import AOS from 'aos';
import { focusHandling } from 'cruip-js-toolkit';

import Home from './pages/Home';
import About from './pages/About';
import SignUp from './pages/SignUp';
import PageNotFound from './pages/PageNotFound';
import InputForm from './pages/InputForm';

function App() {

    const location = useLocation();

    useEffect(() => {
        AOS.init({
            once: true,
            disable: 'phone',
            duration: 600,
            easing: 'ease-out-sine',
        });
    });

    useEffect(() => {
        document.querySelector('html').style.scrollBehavior = 'auto'
        window.scroll({ top: 0 })
        document.querySelector('html').style.scrollBehavior = ''
        focusHandling('outline');
    }, [location.pathname]); // triggered on route change

    return (
        <>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/inputform" element={<InputForm />} />
                {/* <Route path="/features">
          <Features />
        </Route> */}
                {/* <Route path="/pricing">
          <Pricing />
        </Route>
        <Route path="/blog">
          <Blog />
        </Route>
        <Route path="/blog-post">
          <BlogPost />
        </Route> */}
                <Route path="/about" element={<About />} />
                {/* <Route path="/contact">
          <Contact />
        </Route>
        <Route path="/help">
          <Help />
        </Route> */}
                {/* <Route path="/signin">
          <SignIn />
        </Route> */}
                <Route path="/signup" element={<SignUp />} />
                {/* <Route path="/reset-password">
          <ResetPassword />
        </Route> */}
                <Route path="*" element={<PageNotFound />} />
            </Routes >
        </>
    );
}

export default App;
