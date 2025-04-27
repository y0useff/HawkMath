// ========== LaTeX Editor Setup ==========
        
        // Initialize CodeMirror editor
        const editor = CodeMirror.fromTextArea(document.getElementById("latex-editor"), {
            mode: "stex",
            theme: "default",
            lineNumbers: true,
            matchBrackets: true,
            lineWrapping: true,
            autofocus: true
        });
        
        // Auto-resize editor to fit container
        function resizeEditor() {
            const editorElement = editor.getWrapperElement();
            const height = document.getElementById('editor-panel').clientHeight;
            editorElement.style.height = "${height - 20}px";
            editor.refresh();
        }
        
        window.addEventListener('resize', resizeEditor);
        setTimeout(resizeEditor, 100); // Initial resize
        


        // Auto-render on content change (with debounce)
        let renderTimeout;
        editor.on('change', function() {
            clearTimeout(renderTimeout);
            renderTimeout = setTimeout(renderLaTeX, 1000);
        });
        
        // Render function
        function renderLaTeX() {
            const latex = editor.getValue();
            const outputDiv = document.getElementById('output');
            
            outputDiv.innerHTML = latex;
            MathJax.typesetPromise([outputDiv]).catch(err => {
                console.log('MathJax error:', err);
                outputDiv.innerHTML += '<p style="color: red;">Error rendering LaTeX. Check your syntax.</p>';
            });
        }
        
        // Set initial content and render
        setTimeout(renderLaTeX, 500); // Render after MathJax is loaded
        
        // ========== Audio Recorder Setup ==========
        
        let wavesurfer, record;
        let scrollingWaveform = false;
        let continuousWaveform = true;

        
        const createWaveSurfer = () => {
            // Destroy the previous wavesurfer instance
            if (wavesurfer) {
                wavesurfer.destroy();
            }

            // Create a new Wavesurfer instance
            
              

            // Initialize the Record plugin
            record = WaveSurfer.registerPlugin(
                WaveSurfer.Record.create({
                    renderRecordedAudio: false,
                    scrollingWaveform,
                    continuousWaveform,
                    continuousWaveformDuration: 30,
                }),
            );

            

            // Render recorded audio
            record.on('record-end', (blob) => {
                const container = document.createElement('div');
                container.className = 'recording-container';
                document.querySelector('#recordings').prepend(container);
                
                const recordedUrl = URL.createObjectURL(blob);

                // Create wavesurfer from the recorded audio
                const newWavesurfer = WaveSurfer.create({
                    container,
                    waveColor: 'rgb(200, 100, 0)',
                    progressColor: 'rgb(100, 50, 0)',
                    url: recordedUrl,
                });

                // Play button
                const button = container.appendChild(document.createElement('button'));
                button.textContent = 'Play';
                button.onclick = () => newWavesurfer.playPause();
                newWavesurfer.on('pause', () => (button.textContent = 'Play'));
                newWavesurfer.on('play', () => (button.textContent = 'Pause'));

                // Download link
                const link = container.appendChild(document.createElement('a'));
                Object.assign(link, {
                    href: recordedUrl,
                    download: 'hawkmath-recording.' + blob.type.split(';')[0].split('/')[1] || 'webm',
                    textContent: 'Download recording',
                    style: 'margin-left: 10px;'
                });
            });

            pauseButton.style.display = 'none';
            recButton.textContent = 'Record';

            record.on('record-progress', (time) => {
                updateProgress(time);
            });
        }

        const progress = document.querySelector('#progress');
        const updateProgress = (time) => {
            // time will be in milliseconds, convert it to mm:ss format
            const formattedTime = [
                Math.floor((time % 3600000) / 60000), // minutes
                Math.floor((time % 60000) / 1000), // seconds
            ]
                .map((v) => (v < 10 ? '0' + v : v))
                .join(':');
            progress.textContent = formattedTime;
        }

        const pauseButton = document.querySelector('#pause');
        pauseButton.onclick = () => {
            if (record.isPaused()) {
                record.resumeRecording();
                pauseButton.textContent = 'Pause';
                return;
            }

            record.pauseRecording();
            pauseButton.textContent = 'Resume';
        }

        

        // Record button
        const recButton = document.querySelector('#record');

        recButton.onclick = () => {
            if (record.isRecording() || record.isPaused()) {
                record.stopRecording();
                recButton.textContent = 'Record';
                pauseButton.style.display = 'none';
                return;
            }

            recButton.disabled = true;

            // get selected device
            const deviceId = micSelect.value;
            record.startRecording({ deviceId }).then(() => {
                recButton.textContent = 'Stop';
                recButton.disabled = false;
                pauseButton.style.display = 'inline';
            });
        }

        document.querySelector('#scrollingWaveform').onclick = (e) => {
            scrollingWaveform = e.target.checked;
            if (continuousWaveform && scrollingWaveform) {
                continuousWaveform = false;
                document.querySelector('#continuousWaveform').checked = false;
            }
            createWaveSurfer();
        }

        document.querySelector('#continuousWaveform').onclick = (e) => {
            continuousWaveform = e.target.checked;
            if (continuousWaveform && scrollingWaveform) {
                scrollingWaveform = false;
                document.querySelector('#scrollingWaveform').checked = false;
            }
            createWaveSurfer();
        }

        // Initialize on page load
        window.onload = function() {
            createWaveSurfer();
        };