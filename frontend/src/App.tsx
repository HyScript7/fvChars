import type { Component } from "solid-js";
import { Router, Route } from "@solidjs/router";
import Home from "./pages/Home";
import AuthForm from "./components/AuthForm";

const App: Component = () => {
  return (
    <>
      <AuthForm />
      <Router>
        <Route path="/" component={Home} />
      </Router>
    </>
  );
};

export default App;
