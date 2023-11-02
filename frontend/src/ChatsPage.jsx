import { PrettyChatWindow } from "react-chat-engine-pretty";


const ChatsPage = (props) => {
  return (
    <div className="background">
      <PrettyChatWindow
        projectId={"Project ID here"}
        username={props.user.username}
        secret={props.user.secret}
      />
    </div>
  );
};

export default ChatsPage;