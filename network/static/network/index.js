//Render App Component
    function App(){
        const [post,setState] = React.useState(null)
        return(
            <div>
                <NewPost a={post} stateChange ={setState}/>
                <LoadPosts a={post} stateChange ={setState}/>
                
            </div>     

        );     
    }

    //Create Post Component
    function NewPost({a, stateChange}){
        const [state,setState] = React.useState({
            text: ""
        })

        function updateText(event){
            setState({
                text: event.target.value
            });
        }

        function submitText(event){
            fetch('/submit',{
                method:'POST',
                body: JSON.stringify({
                text:state.text

                })
            })
            console.log(state.text)
            setState({
                text: ""
            })
        }
        
        return(
            <div className='container mb-5'>    
                <div className="post">
                    <p className="post-con">New Post</p>
                    <div className="input-group d-flex flex-column">                 
                            <textarea value={state.text} onChange={updateText} className="form-control"></textarea>
                            <button onClick={()=>{
                                submitText()
                                stateChange(!a)
                            }} className="btn btn-primary align-self-start mt-1">Post</button>                           
                    </div>      
                </div>            
            </div>
        );     
    }

    function LoadPosts(props){
        const[posts,setPosts] = React.useState(null)
        const[s_edit, setEdit] = React.useState(null)
        const[edit_id,setId] =React.useState(null)
        const[edit_text,setText]=React.useState('Edit your post here')
        const[username,setU] = React.useState(null)
        const[pageNum,setPageNum] = React.useState(1)
        const[maxPage,setMaxPage] = React.useState(null)
        

        function updateEditText(event){
            setText(event.target.value)
        }

        function like(id){
            console.log(id)
            fetch('/like',{
                method:'POST',
                body:JSON.stringify({
                    post_id: id
                })
            })
            props.stateChange(!props.a)
        }

         function save(id,text){
            fetch('edit',{
                method:'POST',
                body:JSON.stringify({
                    id:id,
                    post:text
                })
            })
            setEdit(false);
            setText('Edit your post here')
        } 
        

        React.useEffect(()=>{
            setTimeout(()=>{
                fetch('post/'+ pageNum)
                .then(response => {return response.json()})
                .then(data =>{
                    setPosts(data.posts)
                    console.log(data.posts)
                    setU(data.username)
                    setMaxPage(data.maxPage)
                });
            },100)
        },[props.a,s_edit,pageNum])

        function next(){
            if(pageNum >= maxPage){
                alert('You are looking last page')
            }else{
                window.scrollTo(0, 0);
                setPageNum(pageNum+1)
            }
            
        }
        function pre(){
            if(pageNum == 1){
                alert('You are looking first page')
            }else{
                window.scrollTo(0, 0);
                setPageNum(pageNum-1)
            }
            
        }

        function edit(id){    

            setEdit(!s_edit)
            setId(id)
        }
        let form = {
            'resize':'none'
        }
        return(
            <div>
                {posts && posts.map((post) =>(
                    <div className=' container post mt-3' key={post.id}>
                        {post.id == edit_id && s_edit && 
                            <div className="input-group d-flex flex-column">
                                <textarea className='mt-3' value={edit_text} onChange={updateEditText}></textarea>
                                <button style={form} className="btn btn-primary align-self-start mt-1" onClick={() => save(post.id,edit_text)}>Save</button>
                            </div>}
                        <Post uname={username} id={post.id} txt={post.p_text} edit_id={edit_id} p_like ={post.p_like} user={post.p_username} s_edit={s_edit} like={like} edit={edit} p_time={post.p_time}/>
                    
                    </div>
                ))}
                <Pages pre={pre} next={next} a={props.a}/>
            </div>
        )
    }

    function Post(props){
        function profile(user){
            window.location = `http://127.0.0.1:8000/profile/${user}`
        }
        return(
            <div className='container d-flex flex-column'>   
                <h5 onClick={()=>profile(props.user)} className='mt-3 p_user' >{props.user}</h5> 
                <p className='p_time lead'>{props.p_time}</p>          
                <p className='Lead'>{props.txt}</p>

                <div className='mb-2 mt-4'>
                    <div className='d-flex justify-content-between'>
                        <div className='d-flex '>
                            <i onClick={() => props.like(props.id)} className="fa fa-heart fa-lg "></i>
                            <p className='align-self-center p_like'>{props.p_like}</p> 
                        </div>
                        
                    </div>
                    {props.user == props.uname && <button className='btn btn-secondary' onClick={() => props.edit(props.id)}>Edit</button>}
                </div>
            </div>
        ) 
    }
    

    function Pages(props){
        let style ={
            'marginRight':'15px',
            'width':'100px'
        }
        return(
            <div className='mt-5 d-flex justify-content-center mb-5'>
                <button className='btn btn-primary' style={style} onClick={props.pre}>previous</button>  
                <button className='btn btn-primary' style={style} onClick={props.next}>next</button>  
            </div>
        )
    }
    
    //Render App
    ReactDOM.render(
        <App />,
        document.getElementById('post')
    )
    </script>
