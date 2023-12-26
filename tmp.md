Creating a mind mapping software with Rust using the Iced framework would be an extensive project, but I can help you get started with a basic setup. Iced is a cross-platform GUI library for Rust, inspired by Elm, that is very suitable for interactive applications like a mind mapping tool.

First, ensure you have Rust installed on your system. If not, install it from the official Rust website (https://www.rust-lang.org/tools/install).

Next, you'll want to create a new project using Cargo, Rust's package manager and build system.

```bash
cargo new mind_mapping --bin
cd mind_mapping
```

Now you need to add Iced as a dependency. Open the `Cargo.toml` file and add Iced under `[dependencies]`.

```toml
[dependencies]
iced = "0.4"
```

Now, let's write a basic Iced application in `main.rs`. Replace the content of `main.rs` with the following code:

```rust
use iced::{
    Application, Column, Command, Element, Settings, Text, button, Button,
};

pub fn main() -> iced::Result {
    MindMapApp::run(Settings::default())
}

struct MindMapApp {
    add_node_button: button::State,
}

#[derive(Debug, Clone)]
enum Message {
    AddNode,
}

impl Application for MindMapApp {
    type Executor = iced::executor::Default;
    type Message = Message;
    type Flags = ();

    fn new(_flags: Self::Flags) -> (Self, Command<Self::Message>) {
        (
            Self {
                add_node_button: button::State::new(),
            },
            Command::none(),
        )
    }

    fn title(&self) -> String {
        String::from("Mind Mapping Application")
    }

    fn update(
        &mut self,
        message: Self::Message,
    ) -> Command<Self::Message> {
        match message {
            Message::AddNode => {
                // Logic for adding a new node to your mind map.
            }
        }

        Command::none()
    }

    fn view(&mut self) -> Element<Self::Message> {
        // Here you define your visual layout and controls
        Column::new()
            .push(
                Text::new("Welcome to the Mind Mapping Application!")
                    .size(30),
            )
            .push(
                Button::new(&mut self.add_node_button, Text::new("Add Node"))
                    .on_press(Message::AddNode),
            )
            .into()
    }
}
```

This is a simple frame to start your application. Currently, the `MindMapApp` struct contains state for a button to add nodes to your mind map. The `Message` enum defines the type of messages your app will handle, which in this case is only adding a new node.

When the "Add Node" button is pressed, an `AddNode` message is sent to the `update` function, where you would define the logic to add new nodes to the mind map.

The `view` function describes what the user interface should look like. It currently generates a column with a welcome text and an "Add Node" button.

As this progresses, you would likely need to add more to your `Message` enum and `MindMapApp` struct, along with more complex update and view logic to handle mind map nodes and their connections.

Once you're ready, you can build and run your project with:

```bash
cargo run
```

From here, you will need more specific functional requirements and UI/UX design to determine what the exact code will look like. Mind mapping software would likely involve graph data structures, complex layout management, and possible persistence for saving and loading maps. You might want to further look into libraries that handle graphs and rendering if Iced's primitives are not sufficient.