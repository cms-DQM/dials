const sleep = seconds => new Promise(r => setTimeout(r, seconds*1000));

export default sleep;
