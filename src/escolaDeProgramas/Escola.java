package escolaDeProgramas;

import javax.swing.Timer;

public class Escola implements Tickavel{
	private Window janela;
	private Timer t;
	public Escola()
	{
		this.janela = new Window();
				
		this.t = new Timer(10, new Tick(this));
		this.t.start();
		
	}
	
	public void tick()
	{
		System.out.println("ta rodando");
	}
}
