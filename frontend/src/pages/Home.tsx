import { Component } from "solid-js";
import { A } from '@solidjs/router'

const Home: Component = () => {
  return (
    <div>
      <p class="text-2xl text-cyan-500">fvChars</p>
      <p><A href="/about" class="link text-cyan-600 hover:text-cyan-700">About</A></p>
    </div>
  );
};

export default Home;
