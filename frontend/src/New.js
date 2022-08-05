import React, { useState } from 'react';
import axios from 'axios';
import "./New.css"
import Modal from './Modal';

function New() {
    const [inputDs, setInputDs] = useState('');
    const [rating, setRating] = useState('');
    const [title, setTitle] = useState('');
    const [modalOpen, setModalOpen] = useState(false);

    const closeModal = () => {
      setModalOpen(false);
    };

    const handleInput = (event) => {
        setInputDs(event.target.value);
    }

    
    const handleKeyPress = (event) => {
        if (event.key === "Enter") {
            onClickInput();
        }
    }

    const onClickInput = async () => {
        setModalOpen(true);
        try {
            console.log("click Login Btn");
            console.log('Input : ', inputDs)
            const response = await axios.post(`http://127.0.0.1:8000/webtoon/${inputDs}`)
            if(response.status === 200) {
                console.log(response.data.recommendation)
                setTitle(response.data.recommendation.title)
                setRating(response.data.recommendation.rating)
            }
        } catch (error) {
            console.dir(error)
        }
        
    }




    return(
        <div className="yurim">
            <h1 className='title'>Webtoon Olympic</h1>
            <h3 className='subtitle'>이 사이트는 Machine Learning 기반의 웹툰 추천 시스템입니다.<br></br>입력해주신 문장을 바탕으로 여러분들에게 웹툰을 추천해드립니다 :D </h3>
            <div>
                <textarea className="box" type = "text" name = "input" value = {inputDs} onChange = {handleInput} onKeyPress = {handleKeyPress} />
            </div>
            <div>
                <button className="button" type="button" onClick={onClickInput}>input</button>
            </div>
            <Modal open={modalOpen} close={closeModal} header="추천 웹툰">
                <div className='recommendedBox'>
                    {Object.values(title)[0]}&nbsp;
                    {Object.values(rating)[0]}
                </div>
                <div className='recommendedBox'>
                    {Object.values(title)[1]}&nbsp;
                    {Object.values(rating)[1]}
                </div>
                <div className='recommendedBox'>
                    {Object.values(title)[2]}&nbsp;
                    {Object.values(rating)[2]}
                </div>
                <div className='recommendedBox'>
                    {Object.values(title)[3]}&nbsp;
                    {Object.values(rating)[3]}
                </div>
                <div className='recommendedBox'>
                    {Object.values(title)[4]}&nbsp;
                    {Object.values(rating)[4]}
                </div>
            </Modal>
        </div>
    )
}

export default New;