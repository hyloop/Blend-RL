<html>
  <body>
    <h1>Blend RL</h1>
    <p>OpenAI gym framework for Blender Game Engine</p>
    <h2>Installation (Ubuntu 18.04 LTS)</h2>
    <p>Extract Blend RL to [blend_rl_folder]. </p>
    <p>Extract blender_2_79b.tar.bz2 to [blender_executable_folder]. </p>
    <p>Open a terminal, run <code>export PATH=$PATH:[blender_executable_folder]</code> to add blender to path temporarily. You may wish to prepend it to ~/.bashrc to add blender to path permanently. </p>
    <p>Run <code>chmod +x [blend_rl_folder]/install</code> to make install executable. </p>
    <h2>Getting started (from minimal working example project)</h2>
    <p>Extract [blend_rl_folder]/minimal_working_example_project.zip to [project_folder]; any folder you have read and write access. </p>
    <p>Run <code>cd [project_folder]</code> to change your current working directory to your project folder. </p>
    <p>Run <code>blender main.blend</code> to open your project. </p>
    <p>Click the "start standalone player" button. </p>
    <p>You should see a moving cube and a static plane. </p>
    <h2>Getting started (from scratch)</h2>
    <p>Create a [project_folder]. </p>
    <p>Run <code>cd [project_folder]</code> to change your current working directory to your project folder. </p>
    <p>Run <code>[blend_rl_folder]/install</code> to install Blend RL into your project. </p>
    <p>Create the agent and environment objects in their respective .blend file. <br/>Create the agent and environment scripts (for mutation) in their respective .py file. </p>
    <p><strong>NOTE: Make a group instance of the agent object. Move the agent object to an inactive layer. </strong></p>
    <p>Create your reinforcement learning algorithm in [project_folder]/main.py. </p>
    <p>Run <code>blender main.blend</code> to open your project. </p>
    <p>Click the "start standalone player" button. </p>
  </body>
</html>
