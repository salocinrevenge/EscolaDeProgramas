package escolaDeProgramas;

import javax.swing.Timer;

public class Escola implements Tickavel{
// essa classe deve conter a escola e todos os seus alunos, alem de seu funcionamento
	private Window janela;
	//possuir a funcao tick e a funcao render
	private Timer t;
	public Escola()
	{
		this.janela = new Window();
				
		this.t = new Timer(10, new Tick(this));
		this.t.start();
		while(true)
		{
			
		}
		
	}
	
	public void tick()
	{
		System.out.println("ta rodando");
	}
}
